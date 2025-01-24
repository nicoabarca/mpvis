import pandas as pd

import mpvis

blasting_event_log_path = "blasting_event_log.csv"

# Read event log
blasting_event_log = pd.read_csv(blasting_event_log_path, sep=";")

# Key is the column format name of pm4py
# Value is the column name of the specific log and soon to be changed to the column name of the event log
# We eill always need 3 columns for case, activity and timestamp
blasting_event_log_format = {
    "case:concept:name": "Case ID",
    "concept:name": "Activity",
    "time:timestamp": "Complete",
    "start_timestamp": "Start",
    "resource": "Resource",
    "cost:total": "Cost",
}

# Format event log
formatted_event_log = mpvis.log_formatter(
    event_log=blasting_event_log, log_format=blasting_event_log_format
)

# Manual log grouping of activities

# The activities to join in a single activity
activities_to_group = [
    "Coordinate verification of poligon pits status",
    "Coordinate terrain revision",
]

# Group the activities
manual_grouped_event_log = mpvis.preprocessing.manual_log_grouping(
    log=formatted_event_log,
    activities_to_group=activities_to_group,
    group_name="Grouped activities",
)


# Prune the log based on the top variants
pruned_event_log = mpvis.preprocessing.prune_log_based_on_top_variants(log=formatted_event_log, k=3)


# MPDFG Functions

# Discover Multi-Perspective DFG

(multi_perspective_dfg, start_activities, end_activities) = (
    mpvis.mpdfg.discover_multi_perspective_dfg(
        log=formatted_event_log,
        calculate_frequency=True,
        calculate_time=True,
        calculate_cost=True,
        frequency_statistic="absolute-activity",
        time_statistic="mean",
        cost_statistic="mean",
    )
)

# Filter Multi-Perspective DFG by activities

activities_filtered_multi_perspective_dfg = mpvis.mpdfg.filter_multi_perspective_dfg_activities(
    percentage=0.5,
    dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    sort_by="frequency",
    ascending=True,
)

# Filter Multi-Perspective DFG by paths

paths_filtered_multi_perspective_dfg = mpvis.mpdfg.filter_multi_perspective_dfg_paths(
    percentage=0.4,
    dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    sort_by="frequency",
    ascending=True,
)

# Get Multi-Perspective DFG string

multi_perspective_dfg_string = mpvis.mpdfg.get_multi_perspective_dfg_string(
    multi_perspective_dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    cost_currency="USD",
    rankdir="TD",
    diagram_tool="graphviz",
)

# View Multi-Perspective DFG

mpvis.mpdfg.view_multi_perspective_dfg(
    multi_perspective_dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    cost_currency="USD",
    rankdir="TD",
    format="svg",
)

# Save Multi-Perspective DFG

mpvis.mpdfg.view_multi_perspective_dfg(
    multi_perspective_dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    file_name="multi_perspective_dfg.svg",
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    cost_currency="USD",
    format="svg",
    rankdir="TD",
    diagram_tool="graphviz",
)


# MDDRT Functions

# Discover Multi-Dimensional DRT

multi_dimensional_drt = mpvis.mddrt.discover_multi_dimensional_drt(
    log=formatted_event_log,
    calculate_time=True,
    calculate_cost=True,
    calculate_quality=True,
    calculate_flexibility=True,
    frequency_statistic="absolute-activity",
    time_statistic="mean",
    cost_statistic="mean",
    group_activities=False,
    show_names=False,
)

# Get Multi-Dimensional DRT string

multi_dimensional_drt_string = mpvis.mddrt.get_multi_dimensional_drt_string(
    multi_dimensional_drt=multi_dimensional_drt,
    visualize_time=True,
    visualize_cost=True,
    visualize_flexibility=True,
    visualize_quality=True,
    node_measures=["total", "consumed", "remaining"],
    arc_measures=["avg", "min", "max"],
)

# View Multi-Dimensional DRT

mpvis.mddrt.view_multi_dimensional_drt(
    multi_dimensional_drt=multi_dimensional_drt,
    visualize_time=True,
    visualize_cost=True,
    visualize_flexibility=True,
    visualize_quality=True,
    node_measures=["total", "consumed", "remaining"],
    arc_measures=["avg", "min", "max"],
    format="svg",
)

# Save Multi-Dimensional DRT diagram

mpvis.mddrt.save_vis_multi_dimensional_drt(
    multi_dimensional_drt=multi_dimensional_drt,
    file_path="multi_dimensional_drt.svg",
    visualize_time=True,
    visualize_cost=True,
    visualize_flexibility=True,
    visualize_quality=True,
    node_measures=["total", "consumed", "remaining"],
    arc_measures=["avg", "min", "max"],
    format="svg",
)
