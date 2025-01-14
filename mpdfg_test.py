import os

import pandas as pd

from mpvis import mpdfg, preprocessing

blasting_event_log_path = os.path.join("data", "blasting_with_rework_event_log.csv")

blasting_event_log = pd.read_csv(blasting_event_log_path, sep=";")

# Key is the column format name of pm4py
# Value is the column name of the specific log and soon to be changed
# We will always need 3 columns for case, activity and timestamp
blasting_format = {
    "case:concept:name": "Case ID",
    "concept:name": "Activity",
    "time:timestamp": "Complete",
    "start_timestamp": "Start",
    "org:resource": "Resource",
    "cost:total": "Cost",
}


blasting_event_log = preprocessing.log_formatter(blasting_event_log, blasting_format)
freq_statistics = ["absolute-activity", "absolute-case", "relative-case", "relative-activity"]
numbers_statistics = ["mean", "min", "max", "stdev", "median", "sum"]
(
    multi_perspective_dfg,
    start_activities,
    end_activities,
) = mpdfg.discover_multi_perspective_dfg(
    blasting_event_log,
    calculate_cost=True,
    calculate_frequency=True,
    calculate_time=True,
    frequency_statistic="absolute-activity",
    time_statistic="mean",
    cost_statistic="max",
)

print(multi_perspective_dfg["activities"])
print(multi_perspective_dfg["connections"])

mpdfg.save_vis_multi_perspective_dfg(
    multi_perspective_dfg,
    start_activities,
    end_activities,
    file_name="data/test",
    visualize_frequency=False,
    visualize_time=True,
    visualize_cost=True,
    format="png",
    rankdir="TB",
    diagram_tool="graphviz",
)
