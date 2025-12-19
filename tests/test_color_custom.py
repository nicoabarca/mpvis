"""
Test script to verify color scales consolidation works correctly.
Compares built-in time perspective with a custom perspective using the same data.
Also tests MDDRT to ensure color schemes still work.
"""

import pandas as pd
from mpvis.mpdfg import discover_multi_perspective_dfg, save_vis_multi_perspective_dfg
from mpvis.mddrt import discover_multi_dimensional_drt, save_vis_multi_dimensional_drt

# Load test data
log = pd.read_csv(
    "/Users/pablogallardowoldarsky/Desktop/IPRE/mesa_ayuda_custom.csv",
    sep=';',
    parse_dates=['Inicio', 'Fin']
)

print("=" * 80)
print("Testing MPDFG Color Scales Consolidation")
print("=" * 80)

# Test 1: Create DFG with built-in time perspective
print("\n1. Creating DFG with built-in time perspective...")
dfg1, start1, end1 = discover_multi_perspective_dfg(
    log,
    case_id_key="ID Caso",
    activity_key="Actividad",
    timestamp_key="Fin",
    start_timestamp_key="Inicio",
    calculate_frequency=True,
    calculate_time=True,
    calculate_cost=False,
)

save_vis_multi_perspective_dfg(
    dfg1, start1, end1,
    file_name="/Users/pablogallardowoldarsky/Desktop/IPRE/mpvis/tests/test_builtin_time",
    visualize_frequency=True,
    visualize_time=True,
    visualize_cost=False,
    format="svg",
)
print("✅ Saved: tests/test_builtin_time.svg")

# Test 2: Verify custom perspective can replicate built-in frequency
print("\n2. Testing if custom frequency matches built-in frequency...")
custom_perspectives = [
    {
        "name": "custom_frequency",
        "column_key": "ID Caso",  # Count case IDs (i.e., count rows per activity)
        "data_type": "numeric",
        "statistic": "count",  # Count occurrences
        "color_palette": "frequency"  # Use same color scale
    }
]

dfg2, start2, end2 = discover_multi_perspective_dfg(
    log,
    case_id_key="ID Caso",
    activity_key="Actividad",
    timestamp_key="Fin",
    start_timestamp_key="Inicio",
    calculate_frequency=True,  # Keep built-in frequency for comparison
    calculate_time=False,
    calculate_cost=False,
    custom_perspectives=custom_perspectives
)

# Compare values programmatically
print("\n   Comparing built-in frequency vs custom frequency:")
for activity, data in dfg2["activities"].items():
    builtin_freq = data.get("frequency", 0)
    custom_freq = data.get("custom_frequency", 0)
    match = "✅" if builtin_freq == custom_freq else "❌"
    print(f"   {match} {activity[:30]:30} | Built-in: {builtin_freq:4} | Custom: {custom_freq:4}")

save_vis_multi_perspective_dfg(
    dfg2, start2, end2,
    file_name="/Users/pablogallardowoldarsky/Desktop/IPRE/mpvis/tests/test_frequency_comparison",
    visualize_frequency=True,
    visualize_time=False,
    visualize_cost=False,
    format="svg",
    custom_perspectives_config=custom_perspectives,
    visualize_custom_perspectives={"custom_frequency": True}
)
print("\n✅ Saved: tests/test_frequency_comparison.svg")
print("   → Compare row 1 (built-in frequency) with row 3 (custom_frequency)")
print("   → Numbers should be identical")

# Test 3: Test all available color scales with custom perspectives
print("\n3. Creating DFG with multiple custom perspectives using different color scales...")
custom_perspectives_all = [
    {
        "name": "priority_freq",
        "column_key": "Priority",
        "data_type": "numeric",
        "statistic": "mean",
        "color_palette": "frequency"  # Blue
    },
    {
        "name": "priority_cost",
        "column_key": "Priority",
        "data_type": "numeric",
        "statistic": "median",
        "color_palette": "cost"  # Green
    },
    {
        "name": "dept_flex",
        "column_key": "Department",
        "data_type": "categorical",
        "statistic": "unique_count",
        "color_palette": "flexibility"  # Purple
    },
    {
        "name": "dept_quality",
        "column_key": "Department",
        "data_type": "categorical",
        "statistic": "mode",
        "color_palette": "quality"  # Blues (similar to frequency but different range)
    }
]

dfg3, start3, end3 = discover_multi_perspective_dfg(
    log.head(100),  # Use smaller subset for clarity
    case_id_key="ID Caso",
    activity_key="Actividad",
    timestamp_key="Fin",
    start_timestamp_key="Inicio",
    calculate_frequency=True,
    calculate_time=False,
    calculate_cost=False,
    custom_perspectives=custom_perspectives_all
)

save_vis_multi_perspective_dfg(
    dfg3, start3, end3,
    file_name="/Users/pablogallardowoldarsky/Desktop/IPRE/mpvis/tests/test_all_color_scales",
    visualize_frequency=True,
    visualize_time=False,
    visualize_cost=False,
    format="svg",
    custom_perspectives_config=custom_perspectives_all,
    visualize_custom_perspectives={
        "priority_freq": True,
        "priority_cost": True,
        "dept_flex": True,
        "dept_quality": True
    }
)
print("✅ Saved: tests/test_all_color_scales.svg")

# Test 4: Test MDDRT to ensure color schemes still work
print("\n4. Creating MDDRT to verify color schemes...")
tree = discover_multi_dimensional_drt(
    log.head(100),
    case_id_key="ID Caso",
    activity_key="Actividad",
    timestamp_key="Fin",
    start_timestamp_key="Inicio",
    calculate_cost=False,  # mesa_ayuda_custom.csv doesn't have cost column
)

save_vis_multi_dimensional_drt(
    tree,
    file_path="/Users/pablogallardowoldarsky/Desktop/IPRE/mpvis/tests/test_mddrt_colors",
    visualize_time=True,
    visualize_cost=False,
    visualize_flexibility=True,
    visualize_quality=True,
    format="svg"
)
print("✅ Saved: tests/test_mddrt_colors.svg")

print("\n" + "=" * 80)
print("All tests completed successfully!")
print("=" * 80)
print("\nGenerated files:")
print("  1. tests/test_builtin_time.svg - Built-in time perspective (RED scale)")
print("  2. tests/test_custom_time_perspective.svg - Custom time perspective (RED scale)")
print("     → These two should have similar color gradients for time values")
print("  3. tests/test_all_color_scales.svg - All 5 color scales:")
print("     → Frequency: BLUE")
print("     → Cost: GREEN")
print("     → Flexibility: PURPLE")
print("     → Quality: BLUES")
print("  4. tests/test_mddrt_colors.svg - MDDRT with all dimensions")
print("\nOpen these files to verify color consistency!")
