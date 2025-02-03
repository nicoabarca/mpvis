import os

import pandas as pd

import mpvis

event_log_path = os.path.join(os.path.dirname(__file__), "data", "merging.csv")

event_log = pd.read_csv(event_log_path, sep=";")

event_log_format = {
    "case:concept:name": "case",
    "concept:name": "activity",
    "time:timestamp": "complete",
    "start_timestamp": "",
    "org:resource": "",
    "cost:total": "cost",
}

processed_log = mpvis.log_formatter(event_log, event_log_format)

processed_log = mpvis.preprocessing.manual_log_grouping(
    processed_log, activities_to_group=["A", "B"]
)

print(processed_log)
