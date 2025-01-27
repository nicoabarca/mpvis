import os

import pandas as pd

import mpvis

event_log_path = os.path.join(
    os.path.dirname(__file__), "data", "LivingLabHospital_Interpreted Location event logs.csv"
)

event_log = pd.read_csv(event_log_path, sep=",")

event_log_format = {
    "case:concept:name": "ID",
    "concept:name": "Activity_MACRO",
    "time:timestamp": "Timestamp end",
    "start_timestamp": "Timestamp start",
    "org:resource": "",
    "cost:total": "",
}

processed_log = mpvis.log_formatter(event_log, event_log_format)

processed_log = mpvis.preprocessing.manual_log_grouping(
    processed_log, activities_to_group=["Registration (Priorities)", "Waiting Room Reception"]
)

drt = mpvis.mddrt.discover_multi_dimensional_drt(processed_log)

mpvis.mddrt.save_vis_multi_dimensional_drt(drt, file_path="hospital_drt")

# processed_log = mpvis.preprocessing.manual_log_grouping(
#     processed_log, activities_to_group=["Registration (normal)", "Waiting Room Reception"]
# )
