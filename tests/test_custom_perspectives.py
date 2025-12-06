"""
Test for custom perspectives in Multi-Perspective DFG.

This test verifies that custom perspectives work correctly with different data types:
- Numeric perspectives (mean, median, etc.)
- Categorical perspectives (mode, unique_count, distribution)
- Timestamp perspectives (duration, mean, etc.)
"""

import os
import tempfile

import pandas as pd
import pytest

from mpvis.mpdfg import discover_multi_perspective_dfg, save_vis_multi_perspective_dfg


@pytest.fixture
def mesa_ayuda_log():
    """Load the mesa_ayuda_custom.csv file with custom columns."""
    # Path to the test CSV file
    csv_path = "/Users/pablogallardowoldarsky/Desktop/IPRE/mesa_ayuda_custom.csv"

    # Check if file exists
    if not os.path.exists(csv_path):
        pytest.skip(f"Test data file not found: {csv_path}")

    # Read the CSV and parse datetime columns
    df = pd.read_csv(
        csv_path,
        sep=';',
        parse_dates=['Inicio', 'Fin']  # Parse timestamp columns as datetime
    )

    # Verify required columns exist
    required_cols = ['ID Caso', 'Actividad', 'Inicio', 'Fin', 'Priority', 'Department']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        pytest.skip(f"Missing required columns: {missing_cols}")

    return df


def test_custom_perspectives_basic(mesa_ayuda_log):
    """Test basic custom perspectives with numeric and categorical data types."""

    # Define custom perspectives
    custom_perspectives = [
        {
            "name": "avg_priority",
            "column_key": "Priority",
            "data_type": "numeric",
            "statistic": "mean",
            "color_palette": "yellow"
        },
        {
            "name": "dept_diversity",
            "column_key": "Department",
            "data_type": "categorical",
            "statistic": "unique_count",
            "color_palette": "purple"
        }
    ]

    # Discover DFG with custom perspectives
    dfg, start_activities, end_activities = discover_multi_perspective_dfg(
        mesa_ayuda_log,
        case_id_key="ID Caso",
        activity_key="Actividad",
        timestamp_key="Fin",
        start_timestamp_key="Inicio",
        calculate_frequency=True,
        calculate_time=True,
        calculate_cost=False,  # No cost column in mesa_ayuda
        custom_perspectives=custom_perspectives
    )

    # Verify DFG structure
    assert "activities" in dfg
    assert "connections" in dfg
    assert len(dfg["activities"]) > 0
    assert len(dfg["connections"]) > 0

    # Verify custom perspectives are present in activities
    first_activity = next(iter(dfg["activities"].values()))
    assert "avg_priority" in first_activity
    assert "dept_diversity" in first_activity

    # Verify custom perspective values are computed
    assert isinstance(first_activity["avg_priority"], (int, float))
    assert isinstance(first_activity["dept_diversity"], int)
    assert first_activity["dept_diversity"] >= 1  # At least 1 unique department

    # Verify built-in perspectives still work
    assert "frequency" in first_activity
    assert "time" in first_activity

    print(f"✅ DFG created with {len(dfg['activities'])} activities")
    print(f"✅ First activity has avg_priority: {first_activity['avg_priority']:.2f}")
    print(f"✅ First activity has {first_activity['dept_diversity']} unique departments")


def test_custom_perspectives_categorical_mode(mesa_ayuda_log):
    """Test categorical perspective with mode statistic."""

    custom_perspectives = [
        {
            "name": "most_common_dept",
            "column_key": "Department",
            "data_type": "categorical",
            "statistic": "mode",
            "color_palette": "purple"
        }
    ]

    # Discover DFG
    dfg, _, _ = discover_multi_perspective_dfg(
        mesa_ayuda_log,
        case_id_key="ID Caso",
        activity_key="Actividad",
        timestamp_key="Fin",
        start_timestamp_key="Inicio",
        calculate_frequency=True,
        calculate_time=False,
        calculate_cost=False,
        custom_perspectives=custom_perspectives
    )

    # Verify mode statistic returns a string (department name)
    first_activity = next(iter(dfg["activities"].values()))
    assert "most_common_dept" in first_activity
    assert isinstance(first_activity["most_common_dept"], str)
    assert first_activity["most_common_dept"] in ['Soporte', 'TI', 'Infraestructura', 'Red', 'Seguridad']

    print(f"✅ Most common department: {first_activity['most_common_dept']}")


def test_custom_perspectives_distribution(mesa_ayuda_log):
    """Test categorical perspective with distribution statistic."""

    custom_perspectives = [
        {
            "name": "dept_distribution",
            "column_key": "Department",
            "data_type": "categorical",
            "statistic": "distribution",
            "color_palette": "purple"
        }
    ]

    # Discover DFG
    dfg, _, _ = discover_multi_perspective_dfg(
        mesa_ayuda_log,
        case_id_key="ID Caso",
        activity_key="Actividad",
        timestamp_key="Fin",
        start_timestamp_key="Inicio",
        calculate_frequency=False,
        calculate_time=False,
        calculate_cost=False,
        custom_perspectives=custom_perspectives
    )

    # Verify distribution statistic returns a formatted string
    first_activity = next(iter(dfg["activities"].values()))
    assert "dept_distribution" in first_activity
    assert isinstance(first_activity["dept_distribution"], str)
    # Should contain percentages
    assert "%" in first_activity["dept_distribution"]

    print(f"✅ Department distribution: {first_activity['dept_distribution']}")


def test_custom_perspectives_multiple_numeric(mesa_ayuda_log):
    """Test multiple numeric perspectives with different statistics."""

    custom_perspectives = [
        {
            "name": "avg_priority",
            "column_key": "Priority",
            "data_type": "numeric",
            "statistic": "mean",
        },
        {
            "name": "max_priority",
            "column_key": "Priority",
            "data_type": "numeric",
            "statistic": "max",
        },
        {
            "name": "min_priority",
            "column_key": "Priority",
            "data_type": "numeric",
            "statistic": "min",
        }
    ]

    # Discover DFG
    dfg, _, _ = discover_multi_perspective_dfg(
        mesa_ayuda_log,
        case_id_key="ID Caso",
        activity_key="Actividad",
        timestamp_key="Fin",
        start_timestamp_key="Inicio",
        calculate_frequency=False,
        calculate_time=False,
        calculate_cost=False,
        custom_perspectives=custom_perspectives
    )

    # Verify all statistics are computed
    first_activity = next(iter(dfg["activities"].values()))
    assert "avg_priority" in first_activity
    assert "max_priority" in first_activity
    assert "min_priority" in first_activity

    # Verify logical relationships
    assert first_activity["min_priority"] <= first_activity["avg_priority"]
    assert first_activity["avg_priority"] <= first_activity["max_priority"]

    print(f"✅ Priority stats - Min: {first_activity['min_priority']}, "
          f"Avg: {first_activity['avg_priority']:.2f}, "
          f"Max: {first_activity['max_priority']}")


def test_custom_perspectives_visualization(mesa_ayuda_log):
    """Test that visualization works with custom perspectives."""

    # Take a small subset for faster testing
    small_log = mesa_ayuda_log.head(100)

    custom_perspectives = [
        {
            "name": "priority",
            "column_key": "Priority",
            "data_type": "numeric",
            "statistic": "mean",
            "color_palette": "gray"
        },
        {
            "name": "departments",
            "column_key": "Department",
            "data_type": "categorical",
            "statistic": "unique_count",
            "color_palette": "purple"
        }
    ]

    # Discover DFG
    dfg, start, end = discover_multi_perspective_dfg(
        small_log,
        case_id_key="ID Caso",
        activity_key="Actividad",
        timestamp_key="Fin",
        start_timestamp_key="Inicio",
        calculate_frequency=True,
        calculate_time=True,
        calculate_cost=False,
        custom_perspectives=custom_perspectives
    )

    # Create file path in tests directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    tmp_path = os.path.join(test_dir, "test_custom_perspectives_dfg")

    try:
        # Save visualization (file_name should be without extension)
        save_vis_multi_perspective_dfg(
            dfg, start, end,
            file_name=tmp_path,
            visualize_frequency=True,
            visualize_time=True,
            visualize_cost=False,
            format="svg",
            custom_perspectives_config=custom_perspectives,
            visualize_custom_perspectives={
                "priority": True,
                "departments": True
            }
        )

        # The actual file will have .svg extension added by graphviz
        actual_path = f"{tmp_path}.svg"

        # Verify file was created
        assert os.path.exists(actual_path), f"File not found at {actual_path}"
        assert os.path.getsize(actual_path) > 0, "File is empty"

        print(f"✅ Visualization created successfully at {actual_path}")

    finally:
        pass # Cleanup created files


def test_custom_perspectives_validation_errors():
    """Test that invalid custom perspective configurations raise appropriate errors."""

    # Test invalid data type
    with pytest.raises(ValueError, match="Invalid data_type"):
        from mpvis.mpdfg.dfg_parameters import CustomPerspective
        CustomPerspective(
            name="test",
            column_key="col",
            data_type="invalid_type",
            statistic="mean"
        )

    # Test invalid statistic for data type
    with pytest.raises(ValueError, match="Invalid statistic"):
        from mpvis.mpdfg.dfg_parameters import CustomPerspective
        CustomPerspective(
            name="test",
            column_key="col",
            data_type="numeric",
            statistic="mode"  # mode is for categorical
        )

    # Test reserved name
    with pytest.raises(ValueError, match="conflicts with built-in"):
        from mpvis.mpdfg.dfg_parameters import CustomPerspective
        CustomPerspective(
            name="frequency",  # Reserved name
            column_key="col",
            data_type="numeric",
            statistic="mean"
        )

    print("✅ All validation errors caught correctly")


if __name__ == "__main__":
    # Run tests manually
    import sys
    sys.path.insert(0, '/Users/pablogallardowoldarsky/Desktop/IPRE/mpvis/src')

    # Load test data with datetime parsing
    log = pd.read_csv(
        "/Users/pablogallardowoldarsky/Desktop/IPRE/mesa_ayuda_custom.csv",
        sep=';',
        parse_dates=['Inicio', 'Fin']
    )

    print("=" * 60)
    print("Running Custom Perspectives Tests")
    print("=" * 60)

    print("\n1. Testing basic custom perspectives...")
    test_custom_perspectives_basic(log)

    print("\n2. Testing categorical mode...")
    test_custom_perspectives_categorical_mode(log)

    print("\n3. Testing distribution statistic...")
    test_custom_perspectives_distribution(log)

    print("\n4. Testing multiple numeric perspectives...")
    test_custom_perspectives_multiple_numeric(log)

    print("\n5. Testing visualization...")
    test_custom_perspectives_visualization(log)

    print("\n6. Testing validation errors...")
    test_custom_perspectives_validation_errors()

    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
