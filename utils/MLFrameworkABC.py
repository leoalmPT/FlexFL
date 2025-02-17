from abc import ABC, abstractmethod
import numpy as np
import random

from utils.DatasetABC import DatasetABC
from utils.NeuralNetworkABC import NeuralNetworkABC


class MLFrameworkABC(ABC):

    def __init__(self, *,
        nn: NeuralNetworkABC,
        dataset: DatasetABC,
        optimizer: str = "adam",
        loss: str = "scc",
        learning_rate: float = 0.001,
        batch_size: int = 1024,
        seed: int = 42,
        **kwargs
    ) -> None:
        self.dataset = dataset
        self.optimizer_name = optimizer
        self.loss_name = loss
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
        self.setup()
        self.model = nn.get_model(self.prefix, dataset)
        self.n_samples = None


    @property
    @abstractmethod
    def prefix(self) -> str:
        """
        Returns the prefix for the ml framework
        """
        pass


    @abstractmethod
    def setup(self):
        """
        Setup the ml environment, e.g. loss, optimizer
        """
        pass


    @abstractmethod
    def load_data(self, split: str) -> None:
        """
        Load the split data and set n_samples
        """
        pass


    @abstractmethod
    def load_worker_data(self, worker_id: int, num_workers: int) -> None:
        """
        Load the data for the worker
        """
        pass


    @abstractmethod
    def compile_model(self) -> None:
        """
        Compile the model
        """
        pass


    @abstractmethod
    def get_weights(self) -> np.array:
        """
        Get the model weights
        """
        pass


    @abstractmethod
    def set_weights(self, weights: np.array) -> None:
        """
        Set the model weights
        """
        pass


    @abstractmethod
    def get_gradients(self) -> np.array:
        """
        Get the model gradients
        """
        pass


    @abstractmethod
    def apply_gradients(self, gradients: np.array) -> None:
        """
        Set the model gradients
        """
        pass


    @abstractmethod
    def train(self, epochs: int) -> None:
        """
        Train the model
        """
        pass


    @abstractmethod
    def predict(self, data: any) -> np.array:
        """
        Predict the data
        """
        pass


    @abstractmethod
    def save_model(self, path: str) -> None:
        """
        Save the model
        """
        pass


    @abstractmethod
    def load_model(self, path: str) -> None:
        """
        Load the model
        """
        pass