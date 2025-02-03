import os

import pandas as pd

import mpvis

event_log_path = os.path.join(
    os.path.dirname(__file__), "data", "blasting_with_rework_event_log.csv"
)

event_log = pd.read_csv(event_log_path, sep=";")

event_log_format = {
    "case:concept:name": "Case ID",
    "concept:name": "Activity",
    "time:timestamp": "Complete",
    "start_timestamp": "Start",
    "org:resource": "Resource",
    "cost:total": "Cost",
}

processed_log = mpvis.log_formatter(event_log, event_log_format)

drt = mpvis.mddrt.discover_multi_dimensional_drt(processed_log)

mpvis.mddrt.view_multi_dimensional_drt(
    drt,
    visualize_cost=True,
    visualize_flexibility=True,
    visualize_quality=True,
    visualize_time=True,
    node_measures=["total"],
    arc_measures=[],
)
