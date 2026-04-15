"""Test script for new table-based arc label format in MD-DRT."""

import pandas as pd
import mpvis

# Create a simple synthetic event log
event_log = pd.DataFrame([
    {"case_id": "C1", "activity": "Register", "start": "2024-01-01 10:00:00", "end": "2024-01-01 10:05:00", "cost": 50},
    {"case_id": "C1", "activity": "Review", "start": "2024-01-01 10:05:00", "end": "2024-01-01 10:15:00", "cost": 100},
    {"case_id": "C1", "activity": "Approve", "start": "2024-01-01 10:15:00", "end": "2024-01-01 10:20:00", "cost": 75},

    {"case_id": "C2", "activity": "Register", "start": "2024-01-01 11:00:00", "end": "2024-01-01 11:06:00", "cost": 55},
    {"case_id": "C2", "activity": "Review", "start": "2024-01-01 11:06:00", "end": "2024-01-01 11:20:00", "cost": 120},
    {"case_id": "C2", "activity": "Approve", "start": "2024-01-01 11:20:00", "end": "2024-01-01 11:25:00", "cost": 80},

    {"case_id": "C3", "activity": "Register", "start": "2024-01-01 12:00:00", "end": "2024-01-01 12:04:00", "cost": 45},
    {"case_id": "C3", "activity": "Review", "start": "2024-01-01 12:04:00", "end": "2024-01-01 12:18:00", "cost": 95},
    {"case_id": "C3", "activity": "Approve", "start": "2024-01-01 12:18:00", "end": "2024-01-01 12:22:00", "cost": 70},
])

# Format the event log
event_log_format = {
    "case:concept:name": "case_id",
    "concept:name": "activity",
    "time:timestamp": "end",
    "start_timestamp": "start",
    "org:resource": "",
    "cost:total": "cost",
}

print("Formatting event log...")
formatted_log = mpvis.log_formatter(log=event_log, log_format=event_log_format)

# Discover Multi-Dimensional DRT
print("Discovering Multi-Dimensional DRT...")
drt = mpvis.mddrt.discover_multi_dimensional_drt(
    log=formatted_log,
    calculate_time=True,
    calculate_cost=True,
    calculate_quality=True,
    calculate_flexibility=True,
    group_activities=False,
    show_names=False,
)

# Generate visualization with the new table format
print("\nGenerating visualization with table-based arc labels...")
print("\nNew table format features:")
print("  ✓ Activity name with frequency in header")
print("  ✓ Dimension sections with colored headers:")
print("    - Time: Orange (#FF6B35)")
print("    - Cost: Green (#4CAF50)")
print("    - Quality: Blue (#2196F3)")
print("    - Flexibility: Purple (#9C27B0)")
print("  ✓ Structured table layout with metric labels and values")
print()

# View the DRT with arc measures enabled (this will show the new table format)
mpvis.mddrt.view_multi_dimensional_drt(
    multi_dimensional_drt=drt,
    visualize_time=True,
    visualize_cost=True,
    visualize_quality=True,
    visualize_flexibility=True,
    node_measures=["total", "consumed", "remaining"],
    arc_measures=["avg", "min", "max"],  # This enables the new table format!
    format="svg",
)

# Save the visualization
print("Saving visualization to file...")
mpvis.mddrt.save_vis_multi_dimensional_drt(
    multi_dimensional_drt=drt,
    file_path="drt_table_format_test.svg",
    visualize_time=True,
    visualize_cost=True,
    visualize_quality=True,
    visualize_flexibility=True,
    node_measures=["total"],
    arc_measures=["avg", "min", "max"],
    format="svg",
)

print("\n✅ Visualization saved as 'drt_table_format_test.svg'")
print("Open the file to see the new table-based arc label format!")
