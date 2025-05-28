import pandas as pd
from pathlib import Path

BASE_DIR = "results/_scenario1"
FILE_NAME = "_analysis/worker_time.csv"
RUN_TIME = "_analysis/run_time.csv"

PROTOCOLS = ["zenoh", "mqtt", "kafka", "mpi"]
FLS = ["da", "ds", "cs", "ca"]

def get_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = pd.DataFrame(columns=df.columns)
    stats.loc[0] = df.mean()
    stats.loc[1] = df.std()
    stats = stats.rename(index={0: "mean", 1: "std"})
    return stats

def print_stats(protocol: str, fl: str):
    worker_times = []
    run_times = []
    for i in range(2, 4 + 1):
        folder = f"{BASE_DIR}/{protocol}_{fl}_{i}"
        if not Path(folder).exists():
            return
        file_path = f"{folder}/{FILE_NAME}"
        worker_times.append(pd.read_csv(file_path))
        run_time_path = f"{folder}/{RUN_TIME}"
        run_times.append(pd.read_csv(run_time_path))
    worker_times_df = pd.concat(worker_times, ignore_index=True)
    worker_times_df = worker_times_df.drop(columns=["Worker"])
    run_times_df = pd.concat(run_times, ignore_index=True)
    run_times_df = run_times_df[["Duration (s)"]]

    print(f"Protocol: {protocol}, FL: {fl}")
    print(get_stats(worker_times_df))
    print(get_stats(run_times_df)) 
    print("\n")


if __name__ == "__main__":
    for fl in FLS:
        for protocol in PROTOCOLS:
            print_stats(protocol, fl)
        print("\n")

