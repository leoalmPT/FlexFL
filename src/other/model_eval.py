import os
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from flexfl.datasets.UNSW import UNSW
from flexfl.datasets.TON_IOT import TON_IOT
from flexfl.neural_nets.UNSW import UNSW as UNSW_NN
from flexfl.neural_nets.TON_IOT import TON_IOT as TON_IOT_NN
from flexfl.ml_fw.Keras import Keras
from flexfl.builtins.FederatedABC import METRICS_FN
from flexfl.builtins.Results import Results


BASE_FOLDER = "results/_scenario3"
DATA = [
    (UNSW, "zenoh_unsw_40", UNSW_NN),
    (TON_IOT, "zenoh_ton_iot_40", TON_IOT_NN),
]
METRICS = ["mcc", "acc", "f1"]

for dataset_cls, folder, nn_cls in DATA:
    folder = f"{BASE_FOLDER}/{folder}"
    res = Results(folder)
    ml = Keras(
        nn=nn_cls(), 
        dataset=dataset_cls()
    )
    ml.load_model(f"{folder}/model")
    ml.load_data(split="test")
    y_true = ml.y_test
    y_pred = ml.predict(ml.x_test)
    y_pred = np.argmax(y_pred, axis=1)
    metrics = {metric: METRICS_FN[metric](y_true, y_pred) for metric in METRICS}
    print(f"Dataset: {dataset_cls.__name__}, Metrics: {metrics}")
    res.plot_cm(y_true, y_pred, show=False)
    