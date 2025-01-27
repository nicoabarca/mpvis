# mpvis

A Python package for Multi-Perspective Process Visualization of event logs

# Index

- [Installation](#installation)
- [Documentation](#documentation)
  - [Event Log Preprocessing](#preprocessing)
  - [Multi-Perspective Directly-Follows Graph (Discovery / Visualization)](#multi-perspective-directly-follows-graph-discovery--visualization)
  - [Multi-Dimensional Directed-Rooted Tree (Discovery / Visualization)](#multi-dimensional-directed-rooted-tree-discovery--visualization)
- [Examples](#examples)

# Installation

This package runs under Python 3.9+, use [pip](https://pip.pypa.io/en/stable/) to install.

```sh
pip install mpvis
```

> **IMPORTANT**
> To render and save generated diagrams, you will also need to install [Graphviz](https://www.graphviz.org)

# Documentation

This package has three main modules:

- `preprocessing` has functionalities for log pruning based on top _k_ variants and manual grouping of log activities.
- `mpdfg` to discover and visualize Multi-Perspective Directly-Follows Graphs (DFG)
- `mddrt` to discover and visualize Multi-Dimensional Directed-Rooted Trees (DRT)

## Event Log Preprocessing

### Format event log

Using `mpvis.log_formatter` you can format your own initial event log with the corresponding column names, based on [pm4py](https://pm4py.fit.fraunhofer.de) standard way of naming logs columns.

The format dictionary to pass as argument to this function needs to have the following structure:

```py
{
    "case:concept:name": <Case Id>, # required
    "concept:name": <Activity Id>, # required
    "time:timestamp": <Timestamp>, # required
    "start_timestamp": <Start Timestamp>, # optional
    "org:resource": <Resource>, # optional
    "cost:total": <Cost>, # optional
}
```

Each value of the dictionary needs to match the corresponding column name of the initial event log. If `start_timestamp`, `org:resource` and `cost:total` are not present in your event log, you can leave its values as blank strings.

```py
import mpvis
import pandas as pd

raw_event_log = pd.read_csv("raw_event_log.csv")

format_dictionary = {
    "case:concept:name": "Case ID",
    "concept:name": "Activity",
    "time:timestamp": "Complete",
    "start_timestamp": "Start",
    "org:resource": "Resource",
    "cost:total": "Cost",
}

event_log = mpvis.log_formatter(raw_event_log, format_dictionary)
```

### Manual log grouping of activities

Groups specified activities in a process log into a single activity group. Every activity name in `activities_to_group` needs to be in the event log activity column.

```py
from mpvis import preprocessing

activities_to_group = ["A", "B", "C"]

manual_grouped_log = preprocessing.manual_log_grouping(
    event_log=event_log,
    activities_to_group=activities_to_group,
    group_name="Grouped Activities" # Optional
    )
```

### Log pruning by number of variants

This function filters the event log to keep only the top k variants based on their frequency. Variants are different sequences of activities in the event log.

```py
from mpvis import preprocessing

#k is the number of variants to keep
pruned_log_by_variants = preprocessing.prune_log_based_on_top_variants(event_log, k=3)
```

## Multi-Perspective Directly-Follows Graph (Discovery / Visualization)

### Discover Multi Perspective DFG

Discovers a multi-perspective Directly-Follows Graph (DFG) from a log.

```py
from mpvis import mpdfg

(
    multi_perspective_dfg,
    start_activities,
    end_activities,
) = mpdfg.discover_multi_perspective_dfg(
    event_log,
    calculate_cost=True,
    calculate_frequency=True,
    calculate_time=True,
    frequency_statistic="absolute-activity", # or absolute-case, relative-activity, relative-case
    time_statistic="mean", # or sum, max, min, stdev, median
    cost_statistic="mean", # or sum, max, min, stdev, median
)

```

### Filter DFG by activities

Filters activities of a multi-perspective Directly-Follows Graph (DFG) diagram.

```py
from mpvis import mpdfg

activities_filtered_multi_perspective_dfg = mpdfg.filter_multi_perspective_dfg_activities(
    percentage=0.5,
    dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    sort_by="frequency",
    ascending=True,
)

```

### Filter DFG by paths

Filters paths of a multi-perspective Directly-Follows Graph (DFG) diagram.

```py
from mpvis import mpdfg

activities_filtered_multi_perspective_dfg = mpdfg.filter_multi_perspective_dfg_paths(
    percentage=0.5,
    dfg=multi_perspective_dfg,
    start_activities=start_activities,
    end_activities=end_activities,
    sort_by="frequency",
    ascending=True,
)

```

### Get the DFG diagram string representation

Creates a string representation of a multi-perspective Directly-Follows Graph (DFG) diagram.

```py
mpdfg_string = mpdfg.get_multi_perspective_dfg_string(
    multi_perspective_dfg,
    start_activities,
    end_activities,
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    rankdir="TB", # or BT, LR, RL, etc.
    diagram_tool="graphviz", # or mermaid
)

```

### View the generated DFG diagram

Allows the user to view the diagram in interactive Python environments like Jupyter and Google Colab.

```py
mpdfg.view_multi_perspective_dfg(
    multi_perspective_dfg,
    start_activities,
    end_activities,
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    rankdir="TB", # or BT, LR, RL, etc.
)
```

### Save the generated DFG diagram

```py
mpdfg.save_vis_multi_perspective_dfg(
    multi_perspective_dfg,
    start_activities,
    end_activities,
    file_name="diagram",
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=True,
    format="png", # or pdf, webp, svg, etc.
    rankdir="TB", # or BT, LR, RL, etc.
    diagram_tool="graphviz", # or mermaid
)
```

# Multi-Dimensional Directed-Rooted Tree (Discovery / Visualization)

### Discover Multi-Dimensional DRT

Discovers and constructs a multi-dimensional Directly Rooted Tree (DRT) from the provided event log.

This function analyzes an event log and creates a multi-dimensional Directly Rooted Tree (DRT)
representing the process model. The DRT is built based on various dimensions such as time, cost,
quality, and flexibility, according to the specified parameters.

```py
from mpvis import mddrt

drt = mddrt.discover_multi_dimensional_drt(
    event_log,
    calculate_cost=True,
    calculate_time=True,
    calculate_flexibility=True,
    calculate_quality=True,
    group_activities=False,
    show_names=False
)
```

### Get the DRT diagram string representation

Generates a string representation of a multi-dimensional directly rooted tree (DRT) diagram.

```py
mddrt_string = mddrt.get_multi_dimension_drt_string(
    multi_dimensional_drt,
    visualize_time=True,
    visualize_cost=True,
    visualize_quality=True,
    visualize_flexibility=True
)
```

### View the generated DRT diagram

Allows the user to view the diagram in interactive Python environments like Jupyter and Google Colab.

```py
mddrt.view_multi_dimensional_drt(
    multi_dimensional_drt
    visualize_time=True,
    visualize_cost=True,
    visualize_quality=True,
    visualize_flexibility=True,
    node_measures=["total"], # accepts also "consumed" and "remaining"
    arc_measures=[], # accepts "avg", "min" and "max", or you can keep this argument empty
    format="svg" # Format value should be a valid image extension like 'jpg', 'png', 'jpeq' or 'webp
)
```

> **WARNING**
> Not all output file formats of Graphviz are available to display in environments like Jupyter Notebook or Google Colab.

### Save the generated DRT diagram

Saves a visualization of a multi-dimensional directly rooted tree (DRT) to a file.

```py
mddrt.save_vis_multi_dimensional_drt(
    multi_dimensional_drt
    file_path="diagram",
    visualize_time=True,
    visualize_cost=True,
    visualize_quality=True,
    visualize_flexibility=True,
    node_measures=["total"], # accepts also "consumed" and "remaining"
    arc_measures=[], # accepts "avg", "min" and "max", or you can keep this argument empty
    format="svg", # or pdf, webp, svg, etc.
)
```

# Examples

Checkout [Examples](https://github.com/nicoabarca/mpdfg/blob/main/examples) to see the package being used to visualize an event log of a mining process.
