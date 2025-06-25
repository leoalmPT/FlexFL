import numpy as np
import time
from rich.console import Console

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
        self.console = Console()
        self.console.print(f"\nJoined with ID: {self.id}\n")


    def setup(self):
        if self.is_master:
            self.ml.load_data("val")
            self.wm.on_worker_disconnect = self.on_worker_disconnect
            self.wm.on_new_worker = self.on_new_worker
        else:
            self.ml.load_data("train")
            self.console.rule("[bold green]Starting Training")
        self.wm.set_callbacks(
            (Task.WORK, self.on_work),
            (Task.WORK_DONE, self.on_work_done)
        )


    def get_worker_info(self) -> dict:
        return {}


    def master_loop(self):
        self.weights = self.ml.get_weights()
        with self.console.status(
            "[bold yellow]Waiting for workers...",
            spinner="dots",
            spinner_style="yellow"
        ) as _:
            self.wm.wait_for_workers(self.min_workers)
        self.console.rule("[bold green]Starting Training")
        self.status = self.console.status(
            f"[bold blue]Epochs done: 0/{self.epochs}[/bold blue] - Tasks done: [yellow]0[/yellow]/[yellow]{self.min_workers}[/yellow]...",
            spinner="dots",
            spinner_style="blue"
        )
        self.status.start()
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
        self.console.rule("[bold green]Training Finished[/bold green]")
        self.status.update(
            "[bold yellow]Waiting for workers to disconnect...",
            spinner="dots",
            spinner_style="yellow"
        )
        self.wm.wait_for(self.finished)
        self.wm.end()
        self.status.stop()
        self.console.print("[bold cyan]Exiting...")


    def handle_iteration(self):
        self.iteration += 1
        epoch = self.iteration // self.min_workers
        current = self.iteration % self.min_workers
        self.status.update(
            f"[bold blue]Epochs done: {epoch}/{self.epochs}[/bold blue] - Tasks done: [yellow]{current}[/yellow]/[yellow]{self.min_workers}[/yellow]...",
            spinner="dots",
            spinner_style="blue"
        )
        if self.iteration % self.min_workers != 0:
            return
        self.ml.set_weights(self.weights)
        metrics, loss, delta_time = self.validate(epoch, split="val", verbose=False)
        self.console.print(
            f"[bold blue]Epoch {epoch}/{self.epochs}[/bold blue] - Time: [bold yellow]{delta_time:.2f}[/bold yellow]s\n"
            f"Loss: [bold yellow]{loss:.4f}[/bold yellow], "
            f"Metrics: {', '.join([f'{k}: {v:.4f}' for k, v in metrics.items()])}\n"
        )
        stop = self.early_stop() or epoch == self.epochs
        if stop:
            Logger.log(Logger.END)
            self.running = False
            

    def on_work(self, sender_id, weights):
        self.console.print(f"[bold yellow]Received Task[/bold yellow] - Sender ID: {sender_id}")
        with self.console.status(
            "[bold yellow]Completing Task...[/bold yellow]",
            spinner="dots",
            spinner_style="yellow"
        ) as _:
            t1 = Logger.log(Logger.WORKING_START)
            self.ml.set_weights(weights)
            self.ml.train(self.local_epochs)
            new_weights = self.ml.get_weights()
            t2 = Logger.log(Logger.WORKING_END)
            self.wm.send(
                node_id = WorkerManager.MASTER_ID, 
                payload = new_weights, 
                type_ = Task.WORK_DONE
            )
        self.console.print(
            f"[bold green]Task Completed[/bold green] - Time: [bold yellow]{t2['timestamp'] - t1['timestamp']:.2f}[/bold yellow]s\n"
        )


    def end(self):
        super().end()
        if not self.is_master:
            self.console.rule("[bold green]Training Finished[/bold green]")


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
        available_workers = set(self.wm.worker_info.keys()) - self.working
        new_worker = self.round_robin_single(available_workers)
        self.working.add(new_worker)
        self.wm.send(
            node_id = new_worker,
            payload = self.weights,
            type_ = Task.WORK
        )


    def on_worker_disconnect(self, worker_id):
        if worker_id not in self.working:
            if self.running:
                self.console.print(f"[bold red]Disconnection[/bold red] - Worker ID: {worker_id} left")
            return
        self.working.remove(worker_id)
        if not self.running:
            return
        self.console.print(f"[bold red]Task Incomplete[/bold red] - Worker ID: {worker_id} left")
        if len(self.wm.worker_info) < self.min_workers:
            self.status.update(
                "[bold yellow]Waiting for workers...[/bold yellow]",
                spinner="dots",
                spinner_style="yellow"
            )
            self.wm.wait_for_workers(self.min_workers)
            epoch = self.iteration // self.min_workers
            current = self.iteration % self.min_workers
            self.status.update(
                f"[bold blue]Epochs done: {epoch}/{self.epochs}[/bold blue] - Tasks done: [yellow]{current}[/yellow]/[yellow]{self.min_workers}[/yellow]...",
                spinner="dots",
                spinner_style="blue"
            )
        self.send_work()


    def linear_interpolation(self, a: np.ndarray, b: np.ndarray, factor: float) -> np.ndarray:
        return a + (b - a)*factor


    def subpool_fn(self, size, worker_info):
        return self.round_robin_pool(size, set(worker_info.keys()))
    

    def finished(self):
        return len(self.working) == 0
    

    def on_new_worker(self, worker_id: int, worker_info: dict) -> None:
        self.console.print(f"[bold green]New worker[/bold green] - Worker ID: {worker_id} joined")
