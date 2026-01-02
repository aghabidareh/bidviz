"""Test configuration and fixtures."""

import numpy as np
import pandas as pd
import pytest

from bidviz import ChartTransformer


@pytest.fixture
def transformer():
    """Provide a ChartTransformer instance for tests."""
    return ChartTransformer()


@pytest.fixture
def sample_kpi_df():
    """Single-row DataFrame for KPI testing."""
    return pd.DataFrame(
        {"total_orders": [150], "total_revenue": [45000.50], "satisfaction_rate": [94.2]}
    )


@pytest.fixture
def sample_bar_df():
    """DataFrame for bar chart testing."""
    return pd.DataFrame(
        {
            "vendor": ["Vendor A", "Vendor B", "Vendor C"],
            "revenue": [125000, 98000, 112000],
            "orders": [450, 380, 420],
        }
    )


@pytest.fixture
def sample_line_df():
    """DataFrame for line chart testing."""
    return pd.DataFrame(
        {"date": pd.date_range("2024-01-01", periods=5), "orders": [152, 168, 145, 175, 160]}
    )


@pytest.fixture
def sample_multi_line_df():
    """DataFrame for multi-line chart testing."""
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=4),
            "vendor_a_orders": [45, 52, 48, 55],
            "vendor_b_orders": [32, 38, 35, 40],
            "vendor_c_orders": [28, 30, 32, 35],
        }
    )


@pytest.fixture
def sample_pie_df():
    """DataFrame for pie chart testing."""
    return pd.DataFrame(
        {"category": ["Electronics", "Clothing", "Food"], "sales": [45000, 32000, 18000]}
    )


@pytest.fixture
def sample_heatmap_df():
    """DataFrame for heatmap testing."""
    return pd.DataFrame(
        {
            "hour": [0, 1, 2, 0, 1, 2],
            "day": ["Monday", "Monday", "Monday", "Tuesday", "Tuesday", "Tuesday"],
            "count": [12, 8, 15, 10, 14, 11],
        }
    )


@pytest.fixture
def sample_table_df():
    """DataFrame for data table testing."""
    return pd.DataFrame(
        {
            "order_id": range(1, 101),
            "customer": [f"Customer {i}" for i in range(1, 101)],
            "amount": np.random.uniform(10, 1000, 100).round(2),
        }
    )


@pytest.fixture
def sample_correlation_df():
    """DataFrame for correlation heatmap testing."""
    np.random.seed(42)
    return pd.DataFrame(
        {
            "revenue": np.random.uniform(1000, 5000, 50),
            "orders": np.random.randint(10, 100, 50),
            "rating": np.random.uniform(3.5, 5.0, 50),
        }
    )


@pytest.fixture
def df_with_nan():
    """DataFrame containing NaN values for testing."""
    return pd.DataFrame({"category": ["A", "B", None, "D"], "value": [100, np.nan, 300, 400]})
