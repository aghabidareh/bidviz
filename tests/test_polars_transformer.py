"""Tests for Polars ChartTransformer class."""

import polars as pl
import pytest

from bidviz.exceptions import TransformationError
from bidviz_polars import ChartTransformer


@pytest.fixture
def polars_transformer():
    """Provide a Polars ChartTransformer instance for tests."""
    return ChartTransformer()


@pytest.fixture
def sample_kpi_df():
    """Single-row Polars DataFrame for KPI testing."""
    return pl.DataFrame(
        {"total_orders": [150], "total_revenue": [45000.50], "satisfaction_rate": [94.2]}
    )


@pytest.fixture
def sample_bar_df():
    """Polars DataFrame for bar chart testing."""
    return pl.DataFrame(
        {
            "vendor": ["Vendor A", "Vendor B", "Vendor C"],
            "revenue": [125000, 98000, 112000],
            "orders": [450, 380, 420],
        }
    )


@pytest.fixture
def sample_line_df():
    """Polars DataFrame for line chart testing."""
    return pl.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "orders": [152, 168, 145, 175, 160],
        }
    )


@pytest.fixture
def sample_multi_line_df():
    """Polars DataFrame for multi-line chart testing."""
    return pl.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
            "vendor_a_orders": [45, 52, 48, 55],
            "vendor_b_orders": [32, 38, 35, 40],
            "vendor_c_orders": [28, 30, 32, 35],
        }
    )


@pytest.fixture
def sample_pie_df():
    """Polars DataFrame for pie chart testing."""
    return pl.DataFrame(
        {"category": ["Electronics", "Clothing", "Food"], "sales": [45000, 32000, 18000]}
    )


@pytest.fixture
def sample_heatmap_df():
    """Polars DataFrame for heatmap testing."""
    return pl.DataFrame(
        {
            "hour": [0, 1, 2, 0, 1, 2],
            "day": ["Monday", "Monday", "Monday", "Tuesday", "Tuesday", "Tuesday"],
            "count": [12, 8, 15, 10, 14, 11],
        }
    )


@pytest.fixture
def sample_table_df():
    """Polars DataFrame for data table testing."""
    return pl.DataFrame(
        {
            "order_id": list(range(1, 101)),
            "customer": [f"Customer {i}" for i in range(1, 101)],
            "amount": [float(i * 10.5) for i in range(1, 101)],
        }
    )


@pytest.fixture
def sample_correlation_df():
    """Polars DataFrame for correlation heatmap testing."""
    return pl.DataFrame(
        {
            "revenue": [1000.0, 2000.0, 1500.0, 2500.0, 3000.0] * 10,
            "orders": [10, 20, 15, 25, 30] * 10,
            "rating": [3.5, 4.0, 4.5, 4.2, 4.8] * 10,
        }
    )


@pytest.fixture
def df_with_null():
    """Polars DataFrame containing null values for testing."""
    return pl.DataFrame(
        {"category": ["A", "B", None, "D"], "value": [100, None, 300, 400]}
    )


class TestKPICards:
    """Tests for transform_to_kpi_cards method."""

    def test_basic_kpi_cards(self, polars_transformer, sample_kpi_df):
        """Test basic KPI cards transformation."""
        result = polars_transformer.transform_to_kpi_cards(sample_kpi_df)

        assert result["chart_type"] == "kpi_cards"
        assert len(result["data"]) == 3
        assert result["data"][0]["key"] == "total_orders"
        assert result["data"][0]["label"] == "Total Orders"
        assert result["data"][0]["value"] == 150

    def test_kpi_with_null(self, polars_transformer):
        """Test KPI cards with null values."""
        df = pl.DataFrame({"metric1": [100], "metric2": [None]})
        result = polars_transformer.transform_to_kpi_cards(df)

        assert result["data"][1]["value"] is None

    def test_kpi_empty_dataframe(self, polars_transformer):
        """Test KPI cards with empty DataFrame."""
        df = pl.DataFrame()
        result = polars_transformer.transform_to_kpi_cards(df)

        assert result["chart_type"] == "kpi_cards"
        assert result["data"] == []

    def test_kpi_multiple_rows_error(self, polars_transformer):
        """Test that multiple rows raise error."""
        df = pl.DataFrame({"metric": [100, 200]})

        with pytest.raises(TransformationError, match="single-row"):
            polars_transformer.transform_to_kpi_cards(df)


class TestBarChart:
    """Tests for transform_to_bar_chart method."""

    def test_basic_bar_chart(self, polars_transformer, sample_bar_df):
        """Test basic bar chart transformation."""
        result = polars_transformer.transform_to_bar_chart(sample_bar_df, "vendor", "revenue")

        assert result["chart_type"] == "bar_chart"
        assert len(result["data"]) == 3
        assert result["data"][0]["x"] == "Vendor A"
        assert result["data"][0]["y"] == 125000
        assert result["x_label"] == "Vendor"
        assert result["y_label"] == "Revenue"

    def test_bar_chart_with_custom_label(self, polars_transformer, sample_bar_df):
        """Test bar chart with custom label column."""
        result = polars_transformer.transform_to_bar_chart(
            sample_bar_df, "vendor", "revenue", label_column="vendor"
        )

        assert result["data"][0]["label"] == "Vendor A"

    def test_bar_chart_missing_column(self, polars_transformer, sample_bar_df):
        """Test bar chart with missing column."""
        with pytest.raises(TransformationError):
            polars_transformer.transform_to_bar_chart(sample_bar_df, "nonexistent", "revenue")

    def test_bar_chart_with_null(self, polars_transformer, df_with_null):
        """Test bar chart with null values."""
        result = polars_transformer.transform_to_bar_chart(df_with_null, "category", "value")

        assert result["data"][1]["y"] is None
        assert result["data"][2]["x"] == "None"


class TestLineChart:
    """Tests for transform_to_line_chart method."""

    def test_basic_line_chart(self, polars_transformer, sample_line_df):
        """Test basic line chart transformation."""
        result = polars_transformer.transform_to_line_chart(sample_line_df, "date", "orders")

        assert result["chart_type"] == "line_chart"
        assert len(result["data"]) == 5
        assert result["series_name"] == "Orders"
        assert result["x_label"] == "Date"
        assert result["y_label"] == "Orders"

    def test_line_chart_custom_series_name(self, polars_transformer, sample_line_df):
        """Test line chart with custom series name."""
        result = polars_transformer.transform_to_line_chart(
            sample_line_df, "date", "orders", series_name="Daily Orders"
        )

        assert result["series_name"] == "Daily Orders"

    def test_line_chart_data_structure(self, polars_transformer, sample_line_df):
        """Test line chart data structure."""
        result = polars_transformer.transform_to_line_chart(sample_line_df, "date", "orders")

        first_point = result["data"][0]
        assert "x" in first_point
        assert "y" in first_point
        assert first_point["y"] == 152

    def test_line_chart_missing_column(self, polars_transformer, sample_line_df):
        """Test line chart with missing column."""
        with pytest.raises(TransformationError):
            polars_transformer.transform_to_line_chart(sample_line_df, "nonexistent", "orders")


class TestMultiLineChart:
    """Tests for transform_to_multi_line_chart method."""

    def test_basic_multi_line(self, polars_transformer, sample_multi_line_df):
        """Test basic multi-line chart transformation."""
        result = polars_transformer.transform_to_multi_line_chart(
            sample_multi_line_df, "date", ["vendor_a_orders", "vendor_b_orders", "vendor_c_orders"]
        )

        assert result["chart_type"] == "multi_line_chart"
        assert len(result["series"]) == 3
        assert result["series"][0]["name"] == "Vendor A Orders"
        assert len(result["series"][0]["data"]) == 4

    def test_multi_line_custom_names(self, polars_transformer, sample_multi_line_df):
        """Test multi-line chart with custom series names."""
        result = polars_transformer.transform_to_multi_line_chart(
            sample_multi_line_df,
            "date",
            ["vendor_a_orders", "vendor_b_orders"],
            series_names=["Vendor Alpha", "Vendor Beta"],
        )

        assert result["series"][0]["name"] == "Vendor Alpha"
        assert result["series"][1]["name"] == "Vendor Beta"

    def test_multi_line_mismatched_names(self, polars_transformer, sample_multi_line_df):
        """Test error when series_names count doesn't match y_columns."""
        with pytest.raises(TransformationError, match="must match"):
            polars_transformer.transform_to_multi_line_chart(
                sample_multi_line_df,
                "date",
                ["vendor_a_orders", "vendor_b_orders"],
                series_names=["Only One Name"],
            )


class TestPieChart:
    """Tests for transform_to_pie_chart method."""

    def test_basic_pie_chart(self, polars_transformer, sample_pie_df):
        """Test basic pie chart transformation."""
        result = polars_transformer.transform_to_pie_chart(sample_pie_df, "category", "sales")

        assert result["chart_type"] == "pie_chart"
        assert len(result["data"]) == 3
        assert result["data"][0]["label"] == "Electronics"
        assert result["data"][0]["value"] == 45000

    def test_pie_chart_missing_column(self, polars_transformer, sample_pie_df):
        """Test pie chart with missing column."""
        with pytest.raises(TransformationError):
            polars_transformer.transform_to_pie_chart(sample_pie_df, "nonexistent", "sales")


class TestHeatmap:
    """Tests for transform_to_heatmap method."""

    def test_basic_heatmap(self, polars_transformer, sample_heatmap_df):
        """Test basic heatmap transformation."""
        result = polars_transformer.transform_to_heatmap(
            sample_heatmap_df, "hour", "day", "count"
        )

        assert result["chart_type"] == "heatmap"
        assert len(result["data"]) == 6
        assert result["x_label"] == "Hour"
        assert result["y_label"] == "Day"
        assert result["value_label"] == "Count"

    def test_heatmap_data_structure(self, polars_transformer, sample_heatmap_df):
        """Test heatmap data structure."""
        result = polars_transformer.transform_to_heatmap(
            sample_heatmap_df, "hour", "day", "count"
        )

        first_point = result["data"][0]
        assert "x" in first_point
        assert "y" in first_point
        assert "value" in first_point


class TestFunnelChart:
    """Tests for transform_to_funnel_chart method."""

    def test_basic_funnel(self, polars_transformer):
        """Test basic funnel chart transformation."""
        df = pl.DataFrame(
            {
                "stage": ["Visits", "Sign-ups", "Purchases", "Repeat Customers"],
                "count": [10000, 3000, 800, 200],
            }
        )
        result = polars_transformer.transform_to_funnel_chart(df, "stage", "count")

        assert result["chart_type"] == "funnel_chart"
        assert len(result["data"]) == 4
        assert result["data"][0]["stage"] == "Visits"
        assert result["data"][0]["value"] == 10000


class TestStackedBarChart:
    """Tests for transform_to_stacked_bar_chart method."""

    def test_basic_stacked_bar(self, polars_transformer):
        """Test basic stacked bar chart transformation."""
        df = pl.DataFrame(
            {
                "month": ["Jan", "Feb", "Mar"],
                "product_a": [100, 150, 120],
                "product_b": [200, 180, 210],
            }
        )
        result = polars_transformer.transform_to_stacked_bar_chart(
            df, "month", ["product_a", "product_b"]
        )

        assert result["chart_type"] == "stacked_bar_chart"
        assert len(result["data"]) == 3
        assert len(result["categories"]) == 2
        assert "Product A" in result["categories"]

    def test_stacked_bar_custom_names(self, polars_transformer):
        """Test stacked bar with custom category names."""
        df = pl.DataFrame(
            {"month": ["Jan", "Feb"], "product_a": [100, 150], "product_b": [200, 180]}
        )
        result = polars_transformer.transform_to_stacked_bar_chart(
            df, "month", ["product_a", "product_b"], category_names=["Alpha", "Beta"]
        )

        assert result["categories"] == ["Alpha", "Beta"]


class TestDataTable:
    """Tests for transform_to_data_table method."""

    def test_basic_table(self, polars_transformer, sample_table_df):
        """Test basic data table transformation."""
        result = polars_transformer.transform_to_data_table(sample_table_df, page=1, page_size=25)

        assert result["chart_type"] == "data_table"
        assert len(result["columns"]) == 3
        assert len(result["rows"]) == 25
        assert result["total"] == 100
        assert result["page"] == 1
        assert result["total_pages"] == 4

    def test_table_pagination(self, polars_transformer, sample_table_df):
        """Test table pagination."""
        result_page_2 = polars_transformer.transform_to_data_table(
            sample_table_df, page=2, page_size=25
        )

        assert result_page_2["page"] == 2
        assert len(result_page_2["rows"]) == 25


class TestCorrelationHeatmap:
    """Tests for transform_to_correlation_heatmap method."""

    def test_basic_correlation(self, polars_transformer, sample_correlation_df):
        """Test basic correlation heatmap transformation."""
        result = polars_transformer.transform_to_correlation_heatmap(sample_correlation_df)

        assert result["chart_type"] == "heatmap"
        assert len(result["metrics"]) == 3
        assert "revenue" in result["metrics"]
        assert result["value_label"] == "Correlation Coefficient"

    def test_correlation_specific_metrics(self, polars_transformer, sample_correlation_df):
        """Test correlation with specific metrics."""
        result = polars_transformer.transform_to_correlation_heatmap(
            sample_correlation_df, metrics=["revenue", "orders"]
        )

        assert len(result["metrics"]) == 2
        assert len(result["data"]) == 4  # 2x2 matrix

    def test_correlation_too_few_columns(self, polars_transformer):
        """Test error when fewer than 2 numeric columns."""
        df = pl.DataFrame({"a": [1, 2, 3]})

        with pytest.raises(TransformationError, match="at least 2"):
            polars_transformer.transform_to_correlation_heatmap(df)
