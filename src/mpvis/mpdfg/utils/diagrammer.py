from datetime import timedelta

from mpvis.utils.color_scales import (
    COST_COLOR_SCALE,
    FLEXIBILITY_COLOR_SCALE,
    FREQUENCY_COLOR_SCALE,
    QUALITY_COLOR_SCALE,
    TIME_COLOR_SCALE,
)


def dimensions_min_and_max(activities, connections) -> tuple[dict, dict]:
    activities_dimensions = next(iter(activities.values())).keys()
    connections_dimensions = next(iter(connections.values())).keys()
    activities_dimensions_min_and_max = {key: (float("inf"), 0) for key in activities_dimensions}
    connections_dimensions_min_and_max = {key: (float("inf"), 0) for key in connections_dimensions}

    for dim in activities_dimensions:
        min_val = min(activity[dim] for activity in activities.values())
        max_val = max(activity[dim] for activity in activities.values())
        # Only apply max(min_val, 0) for numeric values
        if isinstance(min_val, (int, float)):
            activities_dimensions_min_and_max[dim] = (max(min_val, 0), max_val)
        else:
            # For non-numeric values (strings), use a dummy range
            activities_dimensions_min_and_max[dim] = (0, 1)

    for dim in connections_dimensions:
        min_val = min(connection[dim] for connection in connections.values())
        max_val = max(connection[dim] for connection in connections.values())
        # Only apply max(min_val, 0) for numeric values
        if isinstance(min_val, (int, float)):
            connections_dimensions_min_and_max[dim] = (max(min_val, 0), max_val)
        else:
            # For non-numeric values (strings), use a dummy range
            connections_dimensions_min_and_max[dim] = (0, 1)

    return activities_dimensions_min_and_max, connections_dimensions_min_and_max


def ids_mapping(activities):
    mapping = {}
    for idx, activity in enumerate(activities):
        mapping[activity] = f"A{idx}"

    return mapping


def background_color(measure, dimension, dimension_scale, custom_palette_name=None):
    # For non-numeric measures (strings from categorical perspectives), use a default color
    if not isinstance(measure, (int, float)):
        color_palette = color_palette_by_dimension(dimension, custom_palette_name)
        return color_palette[150]  # Use middle color from the palette

    colors_palette_scale = (90, 255)
    color_palette = color_palette_by_dimension(dimension, custom_palette_name)
    assigned_color_index = round(interpolated_value(measure, dimension_scale, colors_palette_scale))
    return color_palette[assigned_color_index]


def color_palette_by_dimension(dimension, custom_palette_name=None):
    # Built-in perspectives
    if dimension == "frequency":
        return FREQUENCY_COLOR_SCALE
    if dimension == "cost":
        return COST_COLOR_SCALE
    if dimension == "time":
        return TIME_COLOR_SCALE

    # Custom perspectives - use palette name or default to available color scales
    if custom_palette_name:
        palette_map = {
            "frequency": FREQUENCY_COLOR_SCALE,
            "cost": COST_COLOR_SCALE,
            "time": TIME_COLOR_SCALE,
            "flexibility": FLEXIBILITY_COLOR_SCALE,
            "quality": QUALITY_COLOR_SCALE,
            "default": FREQUENCY_COLOR_SCALE,
        }
        return palette_map.get(custom_palette_name, FREQUENCY_COLOR_SCALE)

    # Default for unknown dimensions
    return FREQUENCY_COLOR_SCALE


def interpolated_value(measure, from_scale, to_scale):
    measure = max(min(measure, from_scale[1]), from_scale[0])
    denominator = max(1, (from_scale[1] - from_scale[0]))
    normalized_value = (measure - from_scale[0]) / denominator
    interpolated_value = to_scale[0] + normalized_value * (to_scale[1] - to_scale[0])
    return interpolated_value


def format_time(total_seconds):
    delta = timedelta(seconds=total_seconds)
    years = round(delta.days // 365)
    months = round((delta.days % 365) // 30)
    days = round((delta.days % 365) % 30)
    hours = round(delta.seconds // 3600)
    minutes = round((delta.seconds % 3600) // 60)
    seconds = round(delta.seconds % 60)

    if years > 0:
        return f"{years:02d}y {months:02d}m {days:02d}d "
    if months > 0:
        return f"{months:02d}m {days:02d}d {hours:02d}h "
    if days > 0:
        return f"{days:02d}d {hours:02d}h {minutes:02d}m "
    if hours > 0:
        return f"{hours:02d}h {minutes:02d}m {seconds:02d}s "
    if minutes > 0:
        return f"{minutes:02d}m {seconds:02d}s"
    if seconds > 0:
        return f"{seconds:02d}s"
    return "Instant"


def link_width(measure, dimension_scale):
    width_scale = (1, 8)
    link_width = round(interpolated_value(measure, dimension_scale, width_scale), 2)
    return link_width
