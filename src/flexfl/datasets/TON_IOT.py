import pandas as pd
from sklearn.preprocessing import QuantileTransformer

from flexfl.builtins.DatasetABC import DatasetABC


class TON_IOT(DatasetABC):

    @property
    def is_classification(self) -> bool:
        return True
    

    @property
    def scaler(self):
        return QuantileTransformer


    def download(self):
        import kaggle
        kaggle.api.dataset_download_files(
            "dhoogla/nftoniotv2",
            path=f"{self.default_folder}",
            quiet=False,
            unzip=True
        )

    def preprocess(self, val_size, test_size):
        data = pd.read_parquet(f"{self.default_folder}/NF-ToN-IoT-V2.parquet")
        data.dropna()
        y = data['Label'].astype(int)
        x = data.drop(columns=['Label', "L4_SRC_PORT", "L4_DST_PORT", "Attack"])
        self.save_features(x.columns)
        self.split_save(x, y, val_size, test_size)