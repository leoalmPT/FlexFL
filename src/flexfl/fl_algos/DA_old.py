import numpy as np
import time

from flexfl.builtins.FederatedABC import FederatedABC
from flexfl.builtins.WorkerManager import WorkerManager
from flexfl.builtins.Logger import Logger

class Task:
    WORK = 0
    WORK_DONE = 1

class DecentralizedAsync(FederatedABC):

    def __init__(self, *, 
        local_epochs: int = 3,
        da_penalty: float = 0.3,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.local_epochs = local_epochs
        self.penalty = da_penalty
        self.iteration = 0
        self.working = set()


    def setup(self):
        if self.is_master:
            self.ml.load_data("val")
            self.wm.on_worker_disconnect = self.on_worker_disconnect
        else:
            self.ml.load_data("train")
        self.wm.set_callbacks(
            (Task.WORK, self.on_work),
            (Task.WORK_DONE, self.on_work_done)
        )


    def get_worker_info(self) -> dict:
        return {}


    def master_loop(self):
        self.weights = self.ml.get_weights()
        self.wm.wait_for_workers(self.min_workers)
        print("Starting...")
        Logger.log(Logger.START)
        self.epoch_start = time.time()
        pool = self.wm.get_subpool(self.min_workers, self.subpool_fn)
        self.wm.send_n(
            workers = pool, 
            payload = self.weights,
            type_ = Task.WORK
        )
        self.working = set(pool)
        self.run_loop()
        self.wm.wait_for(self.finished)
        self.wm.end()


    def handle_iteration(self):
        self.iteration += 1
        if self.iteration % self.min_workers != 0:
            return
        epoch = self.iteration // self.min_workers
        self.ml.set_weights(self.weights)
        self.validate(epoch, split="val", verbose=True)
        stop = self.early_stop() or epoch == self.epochs
        if stop:
            Logger.log(Logger.END)
            self.running = False
            

    def on_work(self, sender_id, weights):
        Logger.log(Logger.WORKING_START)
        self.ml.set_weights(weights)
        self.ml.train(self.local_epochs)
        new_weights = self.ml.get_weights()
        Logger.log(Logger.WORKING_END)
        self.wm.send(
            node_id = WorkerManager.MASTER_ID, 
            payload = new_weights, 
            type_ = Task.WORK_DONE
        )


    def on_work_done(self, sender_id, worker_weights):
        self.working.discard(sender_id)
        if not self.running:
            return
        self.weights = self.linear_interpolation(
            self.weights, worker_weights, self.penalty
        )
        self.send_work()
        self.handle_iteration()


    def send_work(self):
        avaliable_workers = set(self.wm.worker_info.keys()) - self.working
        new_worker = self.round_robin_single(avaliable_workers)
        self.working.add(new_worker)
        self.wm.send(
            node_id = new_worker,
            payload = self.weights,
            type_ = Task.WORK
        )


    def on_worker_disconnect(self, worker_id):
        if worker_id not in self.working:
            return
        self.working.remove(worker_id)
        if not self.running:
            return
        self.wm.wait_for_workers(self.min_workers)
        self.send_work()


    def linear_interpolation(self, a: np.ndarray, b: np.ndarray, factor: float) -> np.ndarray:
        return a + (b - a)*factor


    def subpool_fn(self, size, worker_info):
        return self.round_robin_pool(size, set(worker_info.keys()))
    

    def finished(self):
        return len(self.working) == 0