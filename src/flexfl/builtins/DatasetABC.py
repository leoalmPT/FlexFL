from abc import ABC, abstractmethod
from pathlib import Path
import json
import numpy as np
from sklearn.model_selection import train_test_split
from typing import Any
import wget
import zipfile
import os


METADATA_FOLDER = Path(__file__).parent.parent / "datasets/_metadata"
DATA_FOLDER = "data"


class DatasetABC(ABC):

    def __init__(self, *,
            data_folder: str = None,
            data_name: str = None,
            **kwargs
        ) -> None:
        self.name = self.__class__.__name__ if data_name is None else data_name
        self.metadata_file = f"{METADATA_FOLDER}/{self.name}.json"
        self.base_path = f"{DATA_FOLDER}/{self.name}"
        self.default_folder = f"{self.base_path}/_data"
        self.output_size = 1
        if data_folder is not None:
            self.data_path = f"{self.base_path}/{data_folder}"
        elif env_folder := os.getenv('DATA_FOLDER') is not None:
            self.data_path = f"{self.base_path}/{env_folder}"
        else:
            self.data_path = self.default_folder
        self.metadata = {}
        self.load_metadata()


    @property
    @abstractmethod
    def is_classification(self) -> bool:
        """
        Returns True if the dataset is a classification dataset
        """
        pass


    @property
    @abstractmethod
    def scaler(self) -> Any:
        """
        Returns the scaler object
        """
        pass


    @abstractmethod
    def download(self):
        """
        Downloads the dataset
        """
        pass


    @abstractmethod
    def preprocess(self, val_size, test_size):
        """
        Preprocesses the dataset
        """
        pass


    def load_metadata(self):
        path = Path(self.metadata_file)
        if path.exists():
            with open(path, 'r') as file:
                self.metadata = json.load(file)
        else:
            self.metadata = {
                "name": self.name, 
                "link": "", 
                "type": "classification" if self.is_classification else "regression", 
                "output_size": self.output_size,
                "info": ""
            }
            self.save_metadata()


    def save_metadata(self):
        with open(self.metadata_file, 'w') as file:
            json.dump(self.metadata, file, indent=4)


    def save_data(self, x, y, split):
        folder = Path(self.data_path)
        folder.mkdir(parents=True, exist_ok=True)
        np.save(folder/f'x_{split}.npy', x)
        np.save(folder/f'y_{split}.npy', y)


    def load_data(self, split, loader = None):
        x: np.ndarray = np.load(f'{self.data_path}/x_{split}.npy')
        y: np.ndarray = np.load(f'{self.data_path}/y_{split}.npy')
        if loader == "tf":
            import tensorflow as tf
            x = tf.data.Dataset.from_tensor_slices(x)
        elif loader == "torch":
            import torch
            x = torch.tensor(x, dtype=torch.float32)
        return x, y
    

    def split_data(self, x, y, val_size, test_size):
        total_size = val_size + test_size
        assert total_size < 1, "val_size + test_size must be less than 1"
        if total_size == 0:
            return x, y, None, None, None, None
        x_train, x_remaining, y_train, y_remaining = train_test_split(
            x, y, 
            test_size=total_size,
            random_state=42, 
            shuffle=True
        )
        if val_size > 0 and test_size > 0:
            x_val, x_test, y_val, y_test = train_test_split(
                x_remaining, y_remaining, 
                test_size=test_size / total_size, 
                random_state=42, 
                shuffle=True
            )
            return x_train, y_train, x_val, y_val, x_test, y_test
        elif val_size > 0:
            return x_train, y_train, x_remaining, y_remaining, None, None
        else:
            return x_train, y_train, None, None, x_remaining, y_remaining

    

    def split_save(self, x, y, val_size = 0.15, test_size = 0.15):
        self.metadata['samples'] = x.shape[0]
        self.metadata['input_shape'] = x.shape[1:]
        if self.is_classification:
            self.output_size = len(np.unique(y))
        self.metadata['output_size'] = self.output_size
        x_train, y_train, x_val, y_val, x_test, y_test = self.split_data(x, y, val_size, test_size)
        self.save_data(x_train, y_train, 'train')
        self.save_data(x_val, y_val, 'val')
        self.save_data(x_test, y_test, 'test')
        self.metadata['split'] = {
            'train': f"{(1-val_size-test_size)*100:.2f}%: {x_train.shape[0]}",
            'val': f"{val_size*100:.2f}%: {x_val.shape[0]}",
            'test': f"{test_size*100:.2f}%: {x_test.shape[0]}"
        }
        self.save_metadata()


    def save_features(self, features):
        self.metadata['features'] = '|'.join(features)
        self.save_metadata()
    

    def data_division(self, num_workers, val_size = 0, test_size = 0):
        for folder in  Path(self.base_path).glob('node_*'):
            for file in folder.glob('*'):
                file.unlink()
            folder.rmdir()
        self.division_master()
        x, y = self.division_iid(num_workers)
        for i in range(num_workers):
            self.division_worker(x[i], y[i], i+1, val_size, test_size)


    def division_master(self):
        self.data_path = self.default_folder
        x, y = self.load_data('val')
        scaler = self.scaler()
        x = scaler.fit_transform(x)
        self.data_path = f"{self.base_path}/node_0"
        self.save_data(x, y, 'val')


    def division_iid(self, num_workers):
        self.data_path = self.default_folder
        x, y = self.load_data('train')
        x = np.array_split(x, num_workers)
        y = np.array_split(y, num_workers)
        return x, y
    

    def division_worker(self, x, y, worker_id, val_size, test_size):
        x_train, y_train, x_val, y_val, x_test, y_test = self.split_data(x, y, val_size, test_size)
        scaler = self.scaler()
        x_train = scaler.fit_transform(x_train)
        self.data_path = f"{self.base_path}/node_{worker_id}"
        self.save_data(x_train, y_train, 'train')
        if val_size > 0:
            x_val = scaler.transform(x_val)
            self.save_data(x_val, y_val, 'val')
        if test_size > 0:
            x_test = scaler.transform(x_test)
            self.save_data(x_test, y_test, 'test')


    def download_file(self, url):
        destination = Path(f"{self.default_folder}/temp.zip")
        destination.parent.mkdir(parents=True, exist_ok=True)
        wget.download(url, str(destination))
        print()
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(destination.parent)
        destination.unlink()