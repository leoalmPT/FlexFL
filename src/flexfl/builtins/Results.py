from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import json
from typing import Generator, Callable
from datetime import datetime
from functools import lru_cache
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio   

pio.kaleido.scope.mathjax = None

IDLE = 0
WORKED = 1
FAILED_IDLE = 2
FAILED_WORKING = 3
FAILED_AFTER_WORKING = 4

STATUS_MAP = {
    IDLE: "Idle without fail",
    WORKED: "Worked successfully<br>without failing",
    FAILED_IDLE: "Failed while idle",
    FAILED_WORKING: "Failed while working",
    FAILED_AFTER_WORKING: "Failed after<br>working successfully"
}


class Results:

    BASE_DIR = "results"

    @staticmethod
    def get_all_folders() -> list[str]:
        folders = Path(Results.BASE_DIR).iterdir()
        folders = sorted(str(f) for f in folders if f.is_dir())
        return folders


    @staticmethod
    def get_last_folder() -> str:
        folders = Results.get_all_folders()
        if len(folders) == 0:
            return None
        return folders[-1]


    def __init__(self, results_folder: str) -> None:
        assert Path(results_folder).is_dir(), f"Results folder {results_folder} does not exist."
        self.results_folder = results_folder
        self.out = f"{results_folder}/_analysis"
        self.logs: dict[int, list[dict]] = {}
        self.log2node: dict[int, int] = {}
        self.setup_paths()
        self.n_workers = len(set(self.log2node.values())) - 1
        if self.n_workers < 1:
            raise ValueError(f"No workers found in results folder {self.results_folder}.")
        Path(self.out).mkdir(parents=True, exist_ok=True)


    def process_path(self, path_: Path, node_id: int = None) -> None:
        if path_.is_file() and path_.name.startswith("log_"):
            log_id = int(path_.name.split("_")[1].split(".")[0])
            if node_id is None:
                node_id = log_id
            self.log2node[log_id] = node_id
            self.logs[log_id] = []
            with open(str(path_), "r") as f:
                for line in f:
                    line = json.loads(line)
                    self.logs[log_id].append(line)


    def setup_paths(self):
        for path_ in Path(self.results_folder).iterdir():
            if path_.is_file():
                self.process_path(path_)
            elif path_.is_dir() and path_.name.startswith("worker_"):
                node_id = int(path_.name.split("_")[1])
                for sub_path in path_.iterdir():
                    self.process_path(sub_path, node_id)
        self.log2node = dict(sorted(self.log2node.items(), key=lambda x: (x[1], x[0])))


    def has_results(self) -> bool:
        return Path(self.out).exists() and len(list(Path(self.out).iterdir())) > 0
    

    def save_results(self, *callbacks: Callable[[], pd.DataFrame]) -> None:
        for callback in callbacks:
            df = callback()
            name = callback.__name__.split("_", 1)[1]
            df.to_csv(f"{self.out}/{name}.csv", index=False)
            df.to_markdown(f"{self.out}/{name}.md", index=False)


    def yield_log(self, log_id: int, events: set = None, fn: Callable[[dict], bool] = None) -> Generator[dict, None, None]:
        assert log_id in self.logs, f"Log {log_id} not found in results folder."
        for line in self.logs[log_id]:
            if (
                (events is not None and line["event"] in events) or
                (fn is not None and fn(line))
            ):
                yield line


    @lru_cache(maxsize=1)
    def get_validations(self) -> pd.DataFrame:
        data = []
        starts = self.yield_log(0, {"validation_start"})
        ends = self.yield_log(0, {"validation_end"})
        for start, end in zip(starts, ends, strict=True):
            data.append((
                datetime.fromtimestamp(start["timestamp"]),
                datetime.fromtimestamp(end["timestamp"]),
                end["timestamp"] - start["timestamp"]
            ))
        return pd.DataFrame(data, columns=["start", "end", "duration"])
    

    def get_generic(self, event: str, log_id: int = None, cols: list[str] = None) -> pd.DataFrame:
        data = []
        if cols is None:
            cols = []
        logs = self.logs if log_id is None else [log_id]
        for id_ in logs:
            for line in self.yield_log(id_, {event}):
                data.append((
                    self.log2node[id_],
                    id_,
                    datetime.fromtimestamp(line["timestamp"]),
                    *(line[col] for col in cols) 
                ))
        df = pd.DataFrame(data, columns=["nid", "lid", "timestamp", *cols])
        df = df.sort_values(by=["timestamp"])
        return df
    

    @lru_cache(maxsize=1)
    def get_failures(self) -> pd.DataFrame:
        df = self.get_generic("failure")
        return df
    

    @lru_cache(maxsize=1)
    def get_joins(self) -> pd.DataFrame:
        df = self.get_generic("join", 0, ["node_id"])
        df = df.drop(columns=["nid", "lid"])
        df = df.rename(columns={"node_id": "lid"})
        df["nid"] = df["lid"].apply(lambda x: self.log2node[x])
        return df
    

    @lru_cache(maxsize=1)
    def get_exits(self) -> pd.DataFrame:
        df = self.get_generic("leave", 0, ["node_id"])
        df = df.drop(columns=["nid", "lid"])
        df = df.rename(columns={"node_id": "lid"})
        df["nid"] = df["lid"].apply(lambda x: self.log2node[x])
        return df
    

    @lru_cache(maxsize=1)
    def get_new_workers(self) -> pd.DataFrame:
        df = self.get_generic("new_worker", 0, ["node_id"])
        df = df.drop(columns=["nid", "lid"])
        df = df.rename(columns={"node_id": "lid"})
        df["nid"] = df["lid"].apply(lambda x: self.log2node[x])
        return df


    @lru_cache(maxsize=1)
    def get_work_times(self) -> pd.DataFrame:
        data = []
        for log_id in self.logs:
            starts = self.yield_log(log_id, {"working_start"})
            ends = self.yield_log(log_id, {"working_end", "failure"})
            for start, end in zip(starts, ends):
                data.append((
                    self.log2node[log_id],
                    log_id,
                    datetime.fromtimestamp(start["timestamp"]),
                    datetime.fromtimestamp(end["timestamp"]),
                    end["timestamp"] - start["timestamp"],
                ))
        df = pd.DataFrame(data, columns=[ "nid", "lid", "start", "end", "duration"])
        df = df.sort_values(by=["nid", "start"])
        return df
    

    @lru_cache(maxsize=1)
    def get_comms(self) -> pd.DataFrame:
        data = []
        for a1, a2, a3 in [("send", "recv", "receiver"), ("recv", "send", "sender")]:
            for log_id in set(self.logs.keys()) - {0}:
                l1s = self.yield_log(0, None, lambda x: x["event"] == a1 and x[a3] == log_id)
                l2s = self.yield_log(log_id, {a2})
                for l1, l2 in zip(l1s, l2s):
                    t1 = l1["timestamp"]
                    t2 = l2["timestamp"]
                    sender = l1["sender"]
                    receiver = l1["receiver"]
                    if a1 == "send":
                        start = t1
                        end = t2
                    else:
                        start = t2
                        end = t1
                    duration = (end - start) * 1000
                    if duration < 0:
                        raise ValueError(f"Negative duration: {duration} ms")
                    data.append((
                        self.log2node[sender],
                        sender,
                        self.log2node[receiver],
                        receiver,
                        datetime.fromtimestamp(start),
                        datetime.fromtimestamp(end),
                        duration,
                        l1["payload_size"]
                    ))
        df = pd.DataFrame(data, columns=["send_nid", "send_lid", "recv_nid", "recv_lid", "start", "end", "duration (ms)", "payload_size (bytes)"])
        df = df.sort_values(by=["start"])
        return df
    

    @lru_cache(maxsize=1)
    def get_metrics(self) -> pd.DataFrame:
        data = []
        logs = self.yield_log(0, {"epoch"})
        for log in logs:
            log = {**log}
            log.pop("event")
            log.pop("timestamp")
            data.append((
                *log.values(),
            ))
        df = pd.DataFrame(data, columns=[*log.keys()])
        df = df.sort_values(by=["epoch"])
        return df
    

    @lru_cache(maxsize=1)
    def get_comms_per_worker(self) -> pd.DataFrame:
        df_ = self.get_comms()
        df_["worker"] = df_.apply(lambda x: max(x["send_nid"], x["recv_nid"]), axis=1)
        df = df_.groupby(["worker"]).agg({
            "duration (ms)": "sum",
            "payload_size (bytes)": "sum",
        })
        df["n_messages"] = df_.groupby(["worker"]).size()
        df = df.reset_index()
        df["payload_size (bytes)"] = df["payload_size (bytes)"] / 1024 / 1024
        df["duration (ms)"] = df["duration (ms)"] / 1000
        df = df.rename(columns={
            "payload_size (bytes)": "payload_size (MB)",
            "duration (ms)": "comm_time (s)"
        })
        df = df.sort_values(by=["worker"])
        return df
    

    @lru_cache(maxsize=1)
    def get_work_time_per_worker(self) -> pd.DataFrame:
        df = self.get_work_times()
        df = df.rename(columns={"nid": "worker"})
        df = df.groupby(["worker"]).agg({
            "duration": "sum",
        })
        df = df.reset_index()
        df = df.rename(columns={
            "duration": "work_time (s)"
        })
        return df
    

    @lru_cache(maxsize=1)
    def get_worker_start_end(self) -> pd.DataFrame:
        data = []
        for log_id in set(self.logs.keys()) - {0}:
            worker_id = self.log2node[log_id]
            start = self.logs[log_id][0]["timestamp"]
            end = self.logs[log_id][-1]["timestamp"]
            data.append((
                worker_id,
                log_id,
                datetime.fromtimestamp(start),
                datetime.fromtimestamp(end),
            ))
        df = pd.DataFrame(data, columns=["nid", "lid", "start", "end"])
        df = df.rename(columns={"nid": "worker"})
        df = df.groupby(["worker"]).agg({
            "start": "min",
            "end": "max",
        })
        df = df.reset_index()
        df["duration"] = df["end"] - df["start"]
        df["duration"] = df["duration"].dt.total_seconds()
        df = df.rename(columns={
            "duration": "total_time (s)"
        })
        df = df.sort_values(by=["worker"])
        return df
    

    @lru_cache(maxsize=1)
    def get_worker_time_status(self) -> pd.DataFrame:
        cpm = self.get_comms_per_worker()
        wtpw = self.get_work_time_per_worker()
        wse = self.get_worker_start_end()
        df = pd.merge(cpm, wtpw, on="worker", how="outer")
        df = pd.merge(df, wse, on="worker", how="outer")
        df["other_time (s)"] = df["total_time (s)"] - df["work_time (s)"] - df["comm_time (s)"]
        df["comm_time% (s)"] = df["comm_time (s)"] / df["total_time (s)"] * 100
        df["work_time% (s)"] = df["work_time (s)"] / df["total_time (s)"] * 100
        df["other_time% (s)"] = df["other_time (s)"] / df["total_time (s)"] * 100
        df = df.drop(columns=["start", "end"])
        return df
    

    @lru_cache(maxsize=1)
    def get_run_time(self) -> pd.DataFrame:
        start = next(self.yield_log(0, {"start"}))
        end = next(self.yield_log(0, {"end"}))
        duration = end["timestamp"] - start["timestamp"]
        data = [(
            datetime.fromtimestamp(start["timestamp"]),
            datetime.fromtimestamp(end["timestamp"]),
            duration,
        )]
        df = pd.DataFrame(data, columns=["Start", "End", "Duration (s)"])
        return df
    

    def calculate_status(self, worker_id: int, epochs: list[tuple[datetime, datetime]]) -> list[int]:
        epoch_status = []
        failures = self.get_failures()
        failures = failures[failures["nid"] == str(worker_id)][["timestamp"]]
        worktimes = self.get_work_times()
        worktimes = worktimes[worktimes["nid"] == worker_id][["start", "end"]]
        for epoch_start, epoch_end in epochs:
            current_status = IDLE
            failure = None
            for _, row in worktimes.iterrows():
                if epoch_start < row["end"] < epoch_end:
                    current_status = WORKED
                    break
            for _, row in failures.iterrows():
                if epoch_start < row["timestamp"] < epoch_end:
                    failure = row["timestamp"]
                    break
            if failure is not None:
                if current_status == IDLE:
                    current_status = FAILED_IDLE
                else:
                    for _, row in worktimes.iterrows():
                        if failure == row["end"]:
                            current_status = FAILED_WORKING
                            break
                    if current_status == WORKED:
                        current_status = FAILED_AFTER_WORKING
            epoch_status.append(current_status)
        return epoch_status
    

    @lru_cache(maxsize=1)
    def get_epochs(self) -> pd.DataFrame:
        validations = self.get_validations()
        epochs = [(
            self.get_run_time().iloc[0]["Start"], 
            validations.iloc[0]["start"]
        )]
        for i in range(1, len(validations)):
            epochs.append((validations.iloc[i-1]["start"], validations.iloc[i]["start"]))
        data = []
        for i, (start, end) in enumerate(epochs):
            data.append({
                "epoch": i + 1,
                "start": start,
                "end": end,
                "duration (s)": (end - start).total_seconds()
            })
        df = pd.DataFrame(data)
        df = df.sort_values(by=["epoch"])
        df = df.reset_index(drop=True)
        df["start"] = pd.to_datetime(df["start"])
        df["end"] = pd.to_datetime(df["end"])
        return df
    

    @lru_cache(maxsize=1)
    def get_worker_status(self) -> pd.DataFrame:
        data = []
        validations = self.get_validations()
        epochs = [(
            self.get_run_time().iloc[0]["Start"], 
            validations.iloc[0]["start"]
        )]
        for i in range(1, len(validations)):
            epochs.append((validations.iloc[i-1]["start"], validations.iloc[i]["start"]))
        
        for nid in range(1, self.n_workers + 1):
            status = self.calculate_status(nid, epochs)
            data.append(status)
        df = pd.DataFrame(data)
        df.index = [f"worker_{i+1}" for i in range(df.shape[0])]
        df.columns = [f"epoch_{i+1}" for i in range(df.shape[1])]
        return df
    

    @lru_cache(maxsize=1)
    def get_overall_status(self) -> pd.DataFrame:
        status = self.get_worker_status()
        df = pd.DataFrame()
        for i in range(len(STATUS_MAP)):
            df[STATUS_MAP[i]] = status.isin([i]).sum(axis=1)
        df = df.reset_index()
        df = df.rename(columns={"index": "Worker"}) 
        df["Non Critical Failures"] = df[[STATUS_MAP[FAILED_IDLE], STATUS_MAP[FAILED_AFTER_WORKING]]].sum(axis=1)
        df["Total Failures"] = df[[STATUS_MAP[FAILED_IDLE], STATUS_MAP[FAILED_WORKING], STATUS_MAP[FAILED_AFTER_WORKING]]].sum(axis=1)
        df["Working times"] = df[[STATUS_MAP[WORKED], STATUS_MAP[FAILED_WORKING], STATUS_MAP[FAILED_AFTER_WORKING]]].sum(axis=1)
        summary_values = df.drop(columns=["Worker"]).sum(numeric_only=True)
        summary_values["Worker"] = "All"
        df.loc[len(df)] = summary_values
        return df


    @lru_cache(maxsize=1)
    def getp_metrics(self) -> pd.DataFrame:
        data = self.get_metrics()
        data = data.rename(columns={
            "mcc": "MCC", 
            "f1": "F1-score", 
            "acc": "Accuracy", 
            "mse": "MSE"
        })
        return data
    

    @lru_cache(maxsize=1)
    def getp_worker_time(self) -> pd.DataFrame:
        df = self.get_worker_time_status()
        df = df[["worker", "payload_size (MB)", "n_messages", "comm_time (s)", "comm_time% (s)", "work_time (s)", "work_time% (s)", "other_time (s)", "other_time% (s)"]]
        df.columns = ["Worker", "Total transfered (MB)", "Total Messages", "Communication Time (s)", "Communication Time (%)", "Work Time (s)", "Work Time (%)", "Other Time (s)", "Other Time (%)"]
        return df
    

    def add_to_timeline(self, fig: go.Figure, df: pd.DataFrame, x: str, y: str, color: str, title: str) -> None:
        df[y] = df[y].astype(str)
        fig.add_trace(go.Scatter(
            x=df[x],
            y=df[y],
            mode="markers",
            name=title,
            marker=dict(
                color=color,
                size=10,
                line=dict(color="black", width=2)
            ), 
        ))
    

    def plot_timeline(self, show = True) -> None:
        worktimes = self.get_work_times()
        failures = self.get_failures()
        joins = self.get_new_workers()
        validations = self.get_validations()
        worktimes = worktimes.rename(columns={"nid": "worker"})
        worktimes = worktimes.sort_values(by=["worker"], ascending=False)
        worktimes["worker"] = worktimes["worker"].astype(str)
        epochs = self.get_epochs()
        epoch_midpoints = epochs["start"] + (epochs["end"] - epochs["start"]) / 2
        epoch_labels = epochs["epoch"].astype(str).tolist()
        fig = px.timeline(
            worktimes,
            x_start="start", 
            x_end="end", 
            y="worker", 
            color="worker", 
            color_discrete_sequence=px.colors.qualitative.Safe,
        )
        for trace in fig.data:
            trace.showlegend = False
        for i, row in validations.iterrows():
            fig.add_shape(
                type="rect",
                x0=row["start"],
                y0=-0.8,
                x1=row["end"],
                y1=self.n_workers-0.2,
                line=dict(color="blue", width=1, dash="dot"),
                showlegend=i==0,
                legendgroup="Validation",
                name="Validation period",
            )

        self.add_to_timeline(fig, failures, "timestamp", "nid", "red", "Failures")
        self.add_to_timeline(fig, joins, "timestamp", "nid", "green", "Joins")
        fig.update_yaxes(title="Workers", title_standoff=5)
        fig.update_xaxes(
            title="Epochs",
            range=[joins["timestamp"].min(), validations["end"].max()],
            tickvals=epoch_midpoints,
            ticktext=epoch_labels,
            tickangle=0
        )
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                title_text="",
            ),
            margin=dict(l=50, r=10, t=0, b=40),
            font=dict(size=16)
        )
        fig.write_image(f"{self.out}/timeline.pdf", width=1200, height=400)
        if show:
            fig.show()


    def plot_training(self, show = True) -> None:
        data = self.getp_metrics()
        metrics = data.columns[-3:]
        fig1 = px.line(
            data,
            x="epoch",
            y="loss",
            labels={"epoch": "Epoch", "loss": "Loss"},
        )
        fig1.update_layout(
            margin=dict(l=60, r=10, t=10, b=50),
            font=dict(size=16),
        )
        fig1.update_yaxes(title_standoff=5)
        fig1.update_xaxes(title_standoff=5)
        fig2 = px.line(
            data,
            x="epoch",
            y=metrics,
            labels={"epoch": "Epoch", "value": "Value"},
        )
        fig2.update_layout(
            margin=dict(l=60, r=10, t=10, b=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                title_text="",
            ),
            font=dict(size=16),
        )
        fig2.update_yaxes(title_standoff=5)
        fig2.update_xaxes(title_standoff=5)
        fig1.write_image(f"{self.out}/validation_loss.pdf", width=600, height=400)
        fig2.write_image(f"{self.out}/validation_metrics.pdf", width=600, height=400)
        if show:
            fig1.show()
            fig2.show()
        

    def plot_times(self, show = True) -> None:
        df = self.get_worker_time_status()
        df_melted = df.melt(
            id_vars="worker", 
            value_vars=["comm_time% (s)", "work_time% (s)", "other_time% (s)"],
            var_name="Time Type", value_name="Percentage"
        )
        label_map = {
            "comm_time% (s)": "Communication",
            "work_time% (s)": "Working",
            "other_time% (s)": "Other"
        }
        df_melted["Time Type"] = df_melted["Time Type"].map(label_map)
        fig = px.bar(
            df_melted,
            x="worker",
            y="Percentage",
            color="Time Type",
            labels={"worker": "Worker", "Percentage": "Time (%)"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig.update_xaxes(tickmode="array", tickvals=df["worker"], ticktext=df["worker"])
        fig.update_yaxes(title="Time (%)", title_standoff=5)
        fig.update_layout(
            barmode="stack",
            margin=dict(l=60, r=20, t=10, b=50),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                title_text="",
            ),
        )
        fig.write_image(f"{self.out}/worker_time.pdf", width=600, height=400)
        if show:
            fig.show()


    def plot_status(self, show = True) -> None:
        df = self.get_worker_status()
        df.index = [f"{i+1}" for i in range(df.shape[0])]
        df.columns = [f"{i+1}" for i in range(df.shape[1])]
        colors = [
            'SteelBlue', 
            'mediumseagreen', 
            'darkorange', 
            'crimson', 
            'DarkGoldenRod'
        ]
        n_colors = len(colors)
        custom_colorscale = []
        for i, color in enumerate(colors):
            custom_colorscale.append([i / n_colors, color])
            custom_colorscale.append([(i + 1) / n_colors, color])
        heatmap_trace = go.Heatmap(
            z=df.values,
            x=df.columns, 
            y=df.index,
            colorscale=custom_colorscale,
            text=df.values,
            xgap=1,
            ygap=1,
            showscale=False,
            zmin=0,
            zmax=len(STATUS_MAP) - 1,
        )
        fig = go.Figure(data=[heatmap_trace])
        for i in range(len(STATUS_MAP)):
            label = STATUS_MAP[i]
            color = colors[i]
            fig.add_trace(go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(size=10, color=color, symbol='square'),
                legendgroup=label,
                showlegend=True,
                name=label,
            ))
        fig.update_layout(
            xaxis_title="Epoch",
            yaxis_title="Worker",
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02,
                title_text="",
            ),
            margin=dict(l=0, r=10, t=10, b=40),
            font=dict(size=16),
        )
        fig.update_yaxes(title_standoff=5)
        fig.update_xaxes(title_standoff=10)
        fig.write_image(f"{self.out}/worker_status.pdf", width=600, height=400)
        if show:
            fig.show()


    def plot_all(self, show = True) -> None:
        try:
            self.plot_times(show)
            self.save_results(
                self.getp_worker_time,
            )
        except Exception as e:
            print(f"Error plotting times: {e}")
        self.plot_timeline(show)
        self.plot_training(show)
        self.plot_status(show)
        self.save_results(
            self.getp_metrics,
            self.get_run_time,
            self.get_overall_status,
        )


    def plot_cm(self, y_true: np.ndarray, y_pred: np.ndarray, labels: list = ["False", "True"], show = True) -> None:
        cm = confusion_matrix(y_true, y_pred)
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=labels,
            y=labels,
            colorscale='Blues',
            zmin=0,
            zmax=np.max(cm),
            xgap=1,
            ygap=1,
            text=cm,
            texttemplate='%{text}',
        ))
        fig.update_layout(
            xaxis_title='Predicted Label',
            yaxis=dict(title="True label", autorange='reversed'),
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(size=12),
        )
        fig.update_xaxes(title_standoff=5)
        fig.update_yaxes(title_standoff=5)
        fig.write_image(f"{self.out}/confusion_matrix.pdf", width=600, height=400)
        if show:
            fig.show()
