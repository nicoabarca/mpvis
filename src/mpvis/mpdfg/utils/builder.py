import numpy as np

DECIMALS_TO_USE = 2


def statistics_names_mapping(dfg_params):
    result = {
        key: getattr(dfg_params, f"{key}_statistic")
        for key in ["frequency", "cost", "time"]
        if getattr(dfg_params, f"calculate_{key}")
    }

    # Add custom perspectives
    if dfg_params.custom_perspectives:
        for perspective in dfg_params.custom_perspectives:
            result[perspective.name] = perspective.statistic

    return result


def new_activity_dict(dfg_params):
    result = {
        key: [] if key != "frequency" else 0
        for key, value in {
            "frequency": dfg_params.calculate_frequency,
            "time": dfg_params.calculate_time,
            "cost": dfg_params.calculate_cost,
        }.items()
        if value
    }

    # Add custom perspectives
    if dfg_params.custom_perspectives:
        for perspective in dfg_params.custom_perspectives:
            # All custom perspectives use lists for data collection
            # (even categorical, as we collect all values before aggregating)
            result[perspective.name] = []

    return result


def new_connection_dict(dfg_params):
    result = {
        key: [] if key != "frequency" else 0
        for key, value in {
            "frequency": dfg_params.calculate_frequency,
            "time": dfg_params.calculate_time,
        }.items()
        if value
    }

    # Add custom perspectives that apply to connections
    if dfg_params.custom_perspectives:
        for perspective in dfg_params.custom_perspectives:
            if perspective.apply_to_connections:
                result[perspective.name] = []

    return result


def absolute_activity(activity_frequency):
    return activity_frequency


def absolute_case(activity_frequency, sum_of_cases):
    return min(activity_frequency, sum_of_cases)


def relative_activity(activity_frequency, sum_of_cases):
    relative_percentage = min(1, activity_frequency / sum_of_cases) * 100
    return round(relative_percentage, DECIMALS_TO_USE)


def relative_case(activity_frequency, sum_of_cases):
    relative_percentage = min(1, activity_frequency / sum_of_cases) * 100
    return round(relative_percentage, DECIMALS_TO_USE)


def mean_val(data):
    return round(np.mean(data), DECIMALS_TO_USE)


def median_val(data):
    return round(np.median(data), DECIMALS_TO_USE)


def sum_val(data):
    return round(np.sum(data), DECIMALS_TO_USE)


def max_val(data):
    return round(np.max(data), DECIMALS_TO_USE)


def min_val(data):
    return round(np.min(data), DECIMALS_TO_USE)


def stdev_val(data):
    return round(np.std(data), DECIMALS_TO_USE)


def count_val(data):
    """Count the number of elements in the data."""
    return len(data)


def mode_val(data):
    """Return the most common value in the data."""
    if not data:
        return None
    from collections import Counter
    counter = Counter(data)
    return counter.most_common(1)[0][0]


def unique_count_val(data):
    """Return the count of unique values in the data."""
    return len(set(data))


def distribution_val(data):
    """Return the distribution of values as a formatted string."""
    if not data:
        return ""
    from collections import Counter
    counter = Counter(data)
    total = len(data)
    # Format: "Value1:50%, Value2:30%, Value3:20%" (top 3 most common)
    return ", ".join([
        f"{val}:{(count/total)*100:.1f}%"
        for val, count in counter.most_common(3)
    ])


def duration_val(data):
    """Calculate duration for timestamp data (difference between max and min)."""
    if not data:
        return 0
    # Assuming data contains timestamps in seconds or timedelta objects
    return round(max(data) - min(data), DECIMALS_TO_USE)


statistics_functions = {
    "absolute-activity": absolute_activity,
    "absolute-case": absolute_case,
    "relative-activity": relative_activity,
    "relative-case": relative_case,
    "mean": mean_val,
    "median": median_val,
    "sum": sum_val,
    "max": max_val,
    "min": min_val,
    "stdev": stdev_val,
    "count": count_val,
    "mode": mode_val,
    "unique_count": unique_count_val,
    "distribution": distribution_val,
    "duration": duration_val,
}
