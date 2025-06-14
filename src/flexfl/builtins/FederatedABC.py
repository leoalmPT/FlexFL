from abc import ABC, abstractmethod
from collections import deque
import json
from pathlib import Path
import time
import numpy as np
from sklearn.metrics import matthews_corrcoef, accuracy_score, f1_score, mean_squared_error, mean_absolute_error
from typing import Callable
import signal
import sys

from flexfl.builtins.WorkerManager import WorkerManager
from flexfl.builtins.MLFrameworkABC import MLFrameworkABC
from flexfl.builtins.Logger import Logger

RESULTS_FOLDER = "results"

METRICS = {
    'classification': [
        'mcc',
        'acc',
        'f1'
    ],
    'regression': [
        'mape',
        'mse',
        'mae'
    ]
}

def smape(y_true, y_pred):
    denominator = (np.abs(y_true) + np.abs(y_pred)) / 2
    smape_values = np.where(denominator == 0, 0, np.abs(y_true - y_pred) / denominator)
    return np.mean(smape_values)

METRICS_FN: dict[str, Callable[[np.ndarray, np.ndarray], float]] = {
    'mcc': matthews_corrcoef,
    'acc': accuracy_score,
    'f1': lambda y_true, y_pred: f1_score(y_true, y_pred, average='weighted'),
    'mape': smape,
    'mse': mean_squared_error,
    'mae': mean_absolute_error
}

class FederatedABC(ABC):

    def __init__(self, *,
        ml: MLFrameworkABC,
        wm: WorkerManager,
        all_args: dict,
        epochs: int = 10,
        target_score: float = None,
        patience: int = 5,
        delta: float = 0.01,
        main_metric: str = None,
        min_workers: int = 2,
        results_folder: str = None,
        base_dir: str = None,
        save_model: bool = True,
        **kwargs
    ) -> None:
        self.ml = ml
        self.wm = wm
        self.all_args = all_args
        self.epochs = epochs
        self.target_score = target_score
        self.patience = patience
        self.delta = delta
        self.main_metric = main_metric
        self.min_workers = min_workers
        self.results_folder = results_folder
        self.base_dir = base_dir
        self.save_model = save_model
        
        self.buffer = deque(maxlen=patience)
        self.compare_score = None
        self.best_score = None
        self.best_weights = None
        self.epoch_start = time.time()
        self.is_classification = None
        self.metrics = None
        self.new_score = None
        self.is_master = None
        self.running = True

        self.rr = set()

        self.setup_metrics()
        self.setup_nodes()
        self.setup_failure()


    @abstractmethod
    def setup(self):
        pass


    @abstractmethod
    def get_worker_info(self) -> dict:
        pass


    @abstractmethod
    def master_loop(self):
        pass


    def setup_metrics(self):
        self.is_classification = self.ml.dataset.is_classification
        if self.target_score is None:
            self.target_score = 1.0 if self.is_classification else 0.0
        all_metrics = METRICS['classification'] if self.is_classification else METRICS['regression']
        if self.main_metric is None:
            self.main_metric = all_metrics[0]
        assert self.main_metric in all_metrics, f"main_metric must be one of {all_metrics}"
        all_metrics.remove(self.main_metric)
        self.metrics = [self.main_metric] + all_metrics

    
    def setup_nodes(self):
        self.id = self.wm.c.id
        self.is_master = self.id == 0
        folder_name = self.wm.c.start_time.strftime('%Y-%m-%d_%H:%M:%S')
        if self.base_dir is not None:
            folder_name = self.base_dir
        if self.results_folder is not None:
            folder_name = f"{folder_name}/{self.results_folder}"
        self.base_path = f"{RESULTS_FOLDER}/{folder_name}"
        Path(self.base_path).mkdir(parents=True, exist_ok=True)
        if self.ml.dataset.default_folder == self.ml.dataset.data_path:
            self.ml.dataset.data_path = f"{self.ml.dataset.base_path}/node_{self.id}"
        Logger.setup(f"{self.base_path}/log_{self.id}.jsonl")
        if self.is_master:
            with open(f"{self.base_path}/args.json", "w") as f:
                json.dump(self.all_args, f, indent=4)
            with open(f"{self.base_path}/.gitignore", "w") as f:
                f.write("*\n")


    def setup_failure(self):
        def handle(signal, frame):
            print()
            if self.is_master:
                self.force_end()
            else:
                Logger.log(Logger.FAILURE)
                self.end()
            sys.exit(0)

        signal.signal(signal.SIGTERM, handle)
        signal.signal(signal.SIGINT, handle)
            

    def run(self):
        self.setup()
        if not self.is_master:
            self.wm.setup_worker_info(self.get_worker_info())
        if self.is_master:
            self.master_loop()
        else:
            self.wm.recv(WorkerManager.EXIT_TYPE)
        self.end()


    def run_loop(self):
        while self.running:
            self.wm.loop_once()
                

    def end(self):
        if self.is_master and self.best_weights is not None and self.save_model:
            self.ml.set_weights(self.best_weights)
            self.ml.save_model(f"{self.base_path}/model")
        self.wm.c.close()
        Logger.end()


    def force_end(self):
        print("Force ending...")
        self.wm.send_n(
            workers = self.wm.get_all_workers(), 
            type_ = WorkerManager.EXIT_TYPE
        )
        self.end()


    def validate(self, epoch: int, split = "val", verbose = False) -> tuple[dict[str, float], float, float]:
        Logger.log(Logger.VALIDATION_START)
        x = getattr(self.ml, f"x_{split}")
        y = getattr(self.ml, f"y_{split}")
        preds = self.ml.predict(x)
        loss = self.ml.calculate_loss(y, preds)
        if self.is_classification:
            preds = np.argmax(preds, axis=1)
        metrics = {name: METRICS_FN[name](y, preds) for name in self.metrics}
        delta_time = time.time() - self.epoch_start
        if verbose:
            print(f"\nEpoch {epoch}/{self.epochs} - Time: {delta_time:.2f}s")
            print(', '.join(f'{name}: {value:.4f}' for name, value in metrics.items()) + f' - Loss: {loss:.4f}')
        self.new_score = metrics[self.metrics[0]]
        if (
            self.best_score is None or
            (self.is_classification and self.new_score > self.best_score) or
            (not self.is_classification and self.new_score < self.best_score)
        ):
            self.best_score = self.new_score
            self.best_weights = self.ml.get_weights()
        Logger.log(Logger.EPOCH, epoch=epoch, time=delta_time, loss=loss, **metrics)
        Logger.log(Logger.VALIDATION_END)
        self.epoch_start = time.time()
        return metrics, loss, delta_time
    

    def early_stop(self) -> bool:
        if (
            (self.is_classification and self.new_score >= self.target_score) or
            (not self.is_classification and self.new_score <= self.target_score)
        ):
            return True

        if len(self.buffer) < self.patience:
            self.buffer.append(self.new_score)
            return False
        
        old_score = self.buffer.popleft()
        if (
            self.compare_score is None or
            (self.is_classification and old_score > self.compare_score) or
            (not self.is_classification and old_score < self.compare_score)
        ):
            self.compare_score = old_score
        
        self.buffer.append(self.new_score)
        if self.is_classification:
            return not any(score >= self.compare_score + self.delta for score in self.buffer)
        else:
            return not any(score <= self.compare_score - self.delta for score in self.buffer)


    def round_robin_single(self, workers: set) -> int:
        assert len(workers) > 0, "No workers available"
        workers_ =  workers - self.rr
        if len(workers_) == 0:
            self.rr = set()
            workers_ = workers
        workers_ = sorted(list(workers_))
        self.rr.add(workers_[0])
        return workers_[0]
        

    def round_robin_pool(self, size: int, workers: set) -> list[int]:
        assert len(workers) >= size, "Not enough workers available"
        chosen = []
        workers_ = workers - self.rr
        if len(workers_) < size:
            chosen = sorted(list(workers_))
            self.rr = set()
        workers_ = workers - set(chosen)
        for _ in range(size - len(chosen)):
            chosen.append(self.round_robin_single(workers_))
        return chosen
