import sys
sys.path.append(".")

from dotenv import load_dotenv
load_dotenv()

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# utils
from Utils.DatasetUtils import DatasetUtils
from Utils.MLUtils import MLUtils
from Utils.FLUtils import FLUtils
from Utils.ModelUtils import ModelUtils

# datasets
from Datasets.IOT_DNL import IOT_DNL
from Datasets.UNSW import UNSW

# models
from Models.IOT_DNL_M1 import IOT_DNL_M1
from Models.UNSW_M1 import UNSW_M1

# ML
from ML.Torch import Torch as MLtorch
from ML.Tensorflow import Tensorflow as MLtf

# Comm
from Comm.MPI import MPI as CommMPI

# FL
from FL.CentralizedSync import CentralizedSync
from FL.DecentralizedSync import DecentralizedSync

# update tf logging level
import tensorflow as tf
tf.get_logger().setLevel('WARN')

print("Config loaded\n")


UTILS = {
    'dataset': DatasetUtils,
    'model': ModelUtils,
    'ml': MLUtils,
    'fl': FLUtils,
}

DATASETS = {
    'IOT_DNL': IOT_DNL,
    'UNSW': UNSW,
}

MODELS = {
    'IOT_DNL': IOT_DNL_M1,
    'UNSW': UNSW_M1,
}

ML = {
    'torch': MLtorch,
    'tf': MLtf
}

COMM = {
    'mpi': CommMPI
}

FL = {
    'cs': CentralizedSync,
    'ds': DecentralizedSync
}
