# mpvis
A Python package for Multi-Perspective Process Visualization of event logs

# Index
- [Installation](#installation)
- [Documentation](#documentation)
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

This package has two main modules:
- `mpdfg` to discover and visualize Multi-Perspective Directly-Follows Graphs (DFG)
- `mddrt` to discover and visualize Multi-Dimensional Directed-Rooted Trees (DRT)

## Multi-Perspective Directly-Follows Graph (Discovery / Visualization)

### Format event log
Using `mpdfg.log_formatter` you can format your own initial event log with the corresponding column names, based on [pm4py](https://pm4py.fit.fraunhofer.de) standard way of naming logs columns.

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
from mpvis import mpdfg
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

event_log = mpdfg.log_formatter(raw_event_log, format_dictionary)

```
### Discover Multi Perspective DFG

```py
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

### Get the DFG diagram string representation
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

### Format event log
Using `mddrt.log_formatter` you can format your own initial event log with the corresponding column names based on [pm4py](https://pm4py.fit.fraunhofer.de) standard way of naming logs columns.

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
from mpvis import mddrt
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

event_log = mddrt.log_formatter(raw_event_log, format_dictionary)

```

### Manual log grouping of activities
Groups specified activities in a process log into a single activity group.

```py
activities_to_group = ["A", "B", "C"]

manual_grouped_log = mddrt.manual_log_grouping(
    event_log=event_log, 
    activities_to_group=activities_to_group,
    group_name="Grouped Activities" # Optional
    )
```
### Log pruning by number of variants
This function filters the event log to keep only the top k variants based on their frequency.Variants are different sequences of activities in the event log.

```py
#k is the number of variants to keep
pruned_log_by_variants = mddrt.prune_log_based_on_top_variants(event_log, k=3) 
```

### Discover Multi-Dimensional DRT

```py
drt = mddrt.discover_multi_dimensional_drt(
    event_log,
    calculate_cost=True,
    calculate_time=True,
    calculate_flexibility=True,
    calculate_quality=True,
    group_activities=False,
)
```

### Automatic group of activities 
```py
grouped_drt = mddrt.group_drt_activities(drt)
```

### Tree pruning by depth
Prunes the tree to the specified maximum depth.
```py
#k is the specified maximum depth 
mddrt.prune_tree_to_depth(drt, k=3) 
```

### Get the DRT diagram string representation
```py
mddrt_string = mpdfg.get_multi_dimension_drt_string(
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
mpdfg.view_multi_dimensional_drt(
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

```py
mpdfg.save_vis_multi_dimensional_drt(
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
