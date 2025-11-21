from dataclasses import dataclass
from typing import Optional


# Valid statistics for each data type
NUMERIC_STATISTICS = {"mean", "median", "sum", "max", "min", "stdev", "count"}
CATEGORICAL_STATISTICS = {"mode", "unique_count", "distribution"}
TIMESTAMP_STATISTICS = {"mean", "median", "min", "max", "duration"}

DATA_TYPE_STATISTICS = {
    "numeric": NUMERIC_STATISTICS,
    "categorical": CATEGORICAL_STATISTICS,
    "timestamp": TIMESTAMP_STATISTICS,
}


@dataclass
class CustomPerspective:
    """
    Defines a custom perspective/dimension to calculate for the DFG.

    Attributes:
        name (str): Name of the perspective (e.g., "resource", "role", "priority")
        column_key (str): Column name in the DataFrame containing the data
        data_type (str): Type of data ("numeric", "categorical", "timestamp")
        statistic (str): Statistic to calculate (depends on data_type)
        apply_to_connections (bool): Whether to apply this perspective to connections/arcs.
                                     Defaults to False.
        color_palette (str): Color palette to use for visualization. Defaults to "default".

    Example:
        CustomPerspective(
            name="resource_count",
            column_key="org:resource",
            data_type="categorical",
            statistic="unique_count",
            apply_to_connections=False
        )
    """
    name: str
    column_key: str
    data_type: str
    statistic: str
    apply_to_connections: bool = False
    color_palette: str = "default"

    def __post_init__(self):
        # Validate data_type
        if self.data_type not in DATA_TYPE_STATISTICS:
            raise ValueError(
                f"Invalid data_type '{self.data_type}'. "
                f"Valid values are: {', '.join(DATA_TYPE_STATISTICS.keys())}"
            )

        # Validate statistic for the given data_type
        valid_statistics = DATA_TYPE_STATISTICS[self.data_type]
        if self.statistic not in valid_statistics:
            raise ValueError(
                f"Invalid statistic '{self.statistic}' for data_type '{self.data_type}'. "
                f"Valid values are: {', '.join(valid_statistics)}"
            )

        # Validate name doesn't conflict with built-in perspectives
        reserved_names = {"frequency", "time", "cost"}
        if self.name.lower() in reserved_names:
            raise ValueError(
                f"Perspective name '{self.name}' conflicts with built-in perspectives. "
                f"Reserved names are: {', '.join(reserved_names)}"
            )


@dataclass
class DirectlyFollowsGraphParameters:
    case_id_key: str = "case:concept:name"
    activity_key: str = "concept:name"
    timestamp_key: str = "time:timestamp"
    start_timestamp_key: str = "start_timestamp"
    cost_key: str = "cost:total"
    calculate_frequency: bool = True
    calculate_time: bool = True
    calculate_cost: bool = True
    frequency_statistic: str = "absolute-activity"
    time_statistic: str = "mean"
    cost_statistic: str = "mean"
    custom_perspectives: Optional[list[CustomPerspective]] = None

    def __post_init__(self):
        if self.frequency_statistic not in {
            "absolute-activity",
            "absolute-case",
            "relative-activity",
            "relative-case",
        }:
            raise ValueError(
                "Valid values for frequency statistic are absolute-activity, absolute-case, relative-activity and relative-case"
            )

        if self.time_statistic not in {"mean", "median", "sum", "max", "min", "stdev"}:
            raise ValueError(
                "Valid values for time statistic are mean, median, sum, max, min and stdev"
            )

        if self.cost_statistic not in {"mean", "median", "sum", "max", "min", "stdev"}:
            raise ValueError(
                "Valid values for cost statistic are mean, median, sum, max, min and stdev"
            )

        # Validate custom perspectives
        if self.custom_perspectives:
            self._validate_custom_perspectives()

    def _validate_custom_perspectives(self):
        """Validate custom perspectives for uniqueness and conflicts."""
        if not self.custom_perspectives:
            return

        # Check for duplicate names
        names = [p.name for p in self.custom_perspectives]
        if len(names) != len(set(names)):
            duplicates = [name for name in names if names.count(name) > 1]
            raise ValueError(
                f"Duplicate custom perspective names found: {', '.join(set(duplicates))}"
            )

        # Note: Individual perspective validation is done in CustomPerspective.__post_init__
