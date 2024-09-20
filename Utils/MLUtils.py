import pprint

from Utils.ModelUtils import ModelUtils
from Utils.DatasetUtils import DatasetUtils

class MLUtils:
    """
    Functions to implement in the child class:
    - init(self)
    - load_data(self, split)
    - load_worker_data(self, worker_id, num_workers)
    - get_weights(self)
    - set_weights(self, weights)
    - get_gradients(self)
    - apply_gradients(self, gradients)
    - train(self, epochs)
    - predict(self, data)
    - save_model(self, path)
    - load_model(self, path)
    """

    def __init__(self, *,
        model: ModelUtils,
        dataset: DatasetUtils,
        optimizer = 'adam',
        loss = 'scc',
        learning_rate = 0.001,
        batch_size = 32,
        **kwargs
    ):
        self.prefix = None
        self.dataset = dataset
        self.optimizer = optimizer
        self.optimizer_name = optimizer
        self.loss = loss
        self.loss_name = loss
        self.learning_rate = learning_rate
        self.batch_size = int(batch_size)
        self.init()
        self.model = model.get_model(self.prefix, self.dataset)
        self.n_samples = None


    def init(self):
        return
    

    def __str__(self):
        return pprint.pformat(vars(self))