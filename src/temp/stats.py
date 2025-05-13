import pandas as pd

BASE_DIR = "results"
FILE_NAME = "_analysis/worker_time.csv"
RUN_TIME = "_analysis/run_time.csv"

PROTOCOL = "kafka"
FOLDERS = f"_{PROTOCOL}_ds"

averages = []
run_times = []

for i in range(1, 4):
    file_path = f"{BASE_DIR}/{FOLDERS}_{i}/{FILE_NAME}"
    df = pd.read_csv(file_path)
    avg = df.mean()
    avg = avg[1:]
    avg = avg.to_dict()
    averages.append(avg)
    run_time_path = f"{BASE_DIR}/{FOLDERS}_{i}/{RUN_TIME}"
    run_time_df = pd.read_csv(run_time_path)
    run_time = run_time_df.iloc[0, -1]
    run_times.append(run_time)

averages_df = pd.DataFrame(averages)
print(averages_df)
print()
print(averages_df.mean())
print()
run_times_df = pd.DataFrame(run_times, columns=["run_time"])
print(run_times_df)
print()
print(run_times_df.mean())