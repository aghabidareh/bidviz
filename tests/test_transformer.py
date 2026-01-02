"""Tests for ChartTransformer class."""

import numpy as np
import pandas as pd
import pytest

from bidviz import ChartTransformer
from bidviz.exceptions import TransformationError


class TestKPICards:
    """Tests for transform_to_kpi_cards method."""

    def test_basic_kpi_cards(self, transformer, sample_kpi_df):
        """Test basic KPI cards transformation."""
        result = transformer.transform_to_kpi_cards(sample_kpi_df)

        assert result["chart_type"] == "kpi_cards"
        assert len(result["data"]) == 3
        assert result["data"][0]["key"] == "total_orders"
        assert result["data"][0]["label"] == "Total Orders"
        assert result["data"][0]["value"] == 150

    def test_kpi_with_nan(self, transformer):
        """Test KPI cards with NaN values."""
        df = pd.DataFrame({"metric1": [100], "metric2": [np.nan]})
        result = transformer.transform_to_kpi_cards(df)

        assert result["data"][1]["value"] is None

    def test_kpi_empty_dataframe(self, transformer):
        """Test KPI cards with empty DataFrame."""
        df = pd.DataFrame()
        result = transformer.transform_to_kpi_cards(df)

        assert result["chart_type"] == "kpi_cards"
        assert result["data"] == []

    def test_kpi_multiple_rows_error(self, transformer):
        """Test that multiple rows raise error."""
        df = pd.DataFrame({"metric": [100, 200]})

        with pytest.raises(TransformationError, match="single-row"):
            transformer.transform_to_kpi_cards(df)


class TestBarChart:
    """Tests for transform_to_bar_chart method."""

    def test_basic_bar_chart(self, transformer, sample_bar_df):
        """Test basic bar chart transformation."""
        result = transformer.transform_to_bar_chart(sample_bar_df, "vendor", "revenue")

        assert result["chart_type"] == "bar_chart"
        assert len(result["data"]) == 3
        assert result["data"][0]["x"] == "Vendor A"
        assert result["data"][0]["y"] == 125000
        assert result["x_label"] == "Vendor"
        assert result["y_label"] == "Revenue"

    def test_bar_chart_with_custom_label(self, transformer, sample_bar_df):
        """Test bar chart with custom label column."""
        result = transformer.transform_to_bar_chart(
            sample_bar_df, "vendor", "revenue", label_column="vendor"
        )

        assert result["data"][0]["label"] == "Vendor A"

    def test_bar_chart_missing_column(self, transformer, sample_bar_df):
        """Test bar chart with missing column."""
        with pytest.raises(TransformationError):
            transformer.transform_to_bar_chart(sample_bar_df, "nonexistent", "revenue")

    def test_bar_chart_with_nan(self, transformer, df_with_nan):
        """Test bar chart with NaN values."""
        result = transformer.transform_to_bar_chart(df_with_nan, "category", "value")

        assert result["data"][1]["y"] is None
        assert result["data"][2]["x"] == "None"


class TestLineChart:
    """Tests for transform_to_line_chart method."""

    def test_basic_line_chart(self, transformer, sample_line_df):
        """Test basic line chart transformation."""
        result = transformer.transform_to_line_chart(sample_line_df, "date", "orders")

        assert result["chart_type"] == "line_chart"
        assert len(result["data"]) == 5
        assert result["series_name"] == "Orders"
        assert result["x_label"] == "Date"
        assert result["y_label"] == "Orders"

    def test_line_chart_custom_series_name(self, transformer, sample_line_df):
        """Test line chart with custom series name."""
        result = transformer.transform_to_line_chart(
            sample_line_df, "date", "orders", series_name="Daily Orders"
        )

        assert result["series_name"] == "Daily Orders"

    def test_line_chart_data_structure(self, transformer, sample_line_df):
        """Test line chart data structure."""
        result = transformer.transform_to_line_chart(sample_line_df, "date", "orders")

        first_point = result["data"][0]
        assert "x" in first_point
        assert "y" in first_point
        assert first_point["y"] == 152

    def test_line_chart_missing_column(self, transformer, sample_line_df):
        """Test line chart with missing column."""
        with pytest.raises(TransformationError):
            transformer.transform_to_line_chart(sample_line_df, "nonexistent", "orders")


class TestMultiLineChart:
    """Tests for transform_to_multi_line_chart method."""

    def test_basic_multi_line(self, transformer, sample_multi_line_df):
        """Test basic multi-line chart transformation."""
        result = transformer.transform_to_multi_line_chart(
            sample_multi_line_df, "date", ["vendor_a_orders", "vendor_b_orders", "vendor_c_orders"]
        )

        assert result["chart_type"] == "multi_line_chart"
        assert len(result["series"]) == 3
        assert result["series"][0]["name"] == "Vendor A Orders"
        assert len(result["series"][0]["data"]) == 4

    def test_multi_line_custom_names(self, transformer, sample_multi_line_df):
        """Test multi-line chart with custom series names."""
        result = transformer.transform_to_multi_line_chart(
            sample_multi_line_df,
            "date",
            ["vendor_a_orders", "vendor_b_orders"],
            series_names=["Vendor Alpha", "Vendor Beta"],
        )

        assert result["series"][0]["name"] == "Vendor Alpha"
        assert result["series"][1]["name"] == "Vendor Beta"

    def test_multi_line_mismatched_names(self, transformer, sample_multi_line_df):
        """Test error when series_names count doesn't match y_columns."""
        with pytest.raises(TransformationError, match="must match"):
            transformer.transform_to_multi_line_chart(
                sample_multi_line_df,
                "date",
                ["vendor_a_orders", "vendor_b_orders"],
                series_names=["Only One Name"],
            )

    def test_multi_line_data_structure(self, transformer, sample_multi_line_df):
        """Test multi-line chart data structure."""
        result = transformer.transform_to_multi_line_chart(
            sample_multi_line_df, "date", ["vendor_a_orders", "vendor_b_orders"]
        )

        first_series = result["series"][0]
        assert "name" in first_series
        assert "data" in first_series
        assert "x" in first_series["data"][0]
        assert "y" in first_series["data"][0]


class TestPieChart:
    """Tests for transform_to_pie_chart method."""

    def test_basic_pie_chart(self, transformer, sample_pie_df):
        """Test basic pie chart transformation."""
        result = transformer.transform_to_pie_chart(sample_pie_df, "category", "sales")

        assert result["chart_type"] == "pie_chart"
        assert len(result["data"]) == 3
        assert result["data"][0]["label"] == "Electronics"
        assert result["data"][0]["value"] == 45000

    def test_pie_chart_data_structure(self, transformer, sample_pie_df):
        """Test pie chart data structure."""
        result = transformer.transform_to_pie_chart(sample_pie_df, "category", "sales")

        for item in result["data"]:
            assert "label" in item
            assert "value" in item

    def test_pie_chart_missing_column(self, transformer, sample_pie_df):
        """Test pie chart with missing column."""
        with pytest.raises(TransformationError):
            transformer.transform_to_pie_chart(sample_pie_df, "nonexistent", "sales")


class TestHeatmap:
    """Tests for transform_to_heatmap method."""

    def test_basic_heatmap(self, transformer, sample_heatmap_df):
        """Test basic heatmap transformation."""
        result = transformer.transform_to_heatmap(sample_heatmap_df, "hour", "day", "count")

        assert result["chart_type"] == "heatmap"
        assert len(result["data"]) == 6
        assert result["x_label"] == "Hour"
        assert result["y_label"] == "Day"
        assert result["value_label"] == "Count"

    def test_heatmap_data_structure(self, transformer, sample_heatmap_df):
        """Test heatmap data structure."""
        result = transformer.transform_to_heatmap(sample_heatmap_df, "hour", "day", "count")

        first_point = result["data"][0]
        assert "x" in first_point
        assert "y" in first_point
        assert "value" in first_point

    def test_heatmap_missing_column(self, transformer, sample_heatmap_df):
        """Test heatmap with missing column."""
        with pytest.raises(TransformationError):
            transformer.transform_to_heatmap(sample_heatmap_df, "hour", "day", "nonexistent")


class TestFunnelChart:
    """Tests for transform_to_funnel_chart method."""

    def test_basic_funnel(self, transformer):
        """Test basic funnel chart transformation."""
        df = pd.DataFrame({"stage": ["Visits", "Sign-ups", "Purchases"], "count": [1000, 300, 100]})
        result = transformer.transform_to_funnel_chart(df, "stage", "count")

        assert result["chart_type"] == "funnel_chart"
        assert len(result["data"]) == 3
        assert result["data"][0]["stage"] == "Visits"
        assert result["data"][0]["value"] == 1000

    def test_funnel_data_structure(self, transformer):
        """Test funnel chart data structure."""
        df = pd.DataFrame({"stage": ["A", "B"], "value": [100, 50]})
        result = transformer.transform_to_funnel_chart(df, "stage", "value")

        for item in result["data"]:
            assert "stage" in item
            assert "value" in item


class TestStackedBarChart:
    """Tests for transform_to_stacked_bar_chart method."""

    def test_basic_stacked_bar(self, transformer):
        """Test basic stacked bar chart transformation."""
        df = pd.DataFrame(
            {
                "month": ["Jan", "Feb", "Mar"],
                "product_a": [100, 150, 120],
                "product_b": [200, 180, 210],
            }
        )
        result = transformer.transform_to_stacked_bar_chart(df, "month", ["product_a", "product_b"])

        assert result["chart_type"] == "stacked_bar_chart"
        assert len(result["data"]) == 3
        assert len(result["categories"]) == 2
        assert result["data"][0]["x"] == "Jan"
        assert result["data"][0]["product_a"] == 100

    def test_stacked_bar_custom_names(self, transformer):
        """Test stacked bar with custom category names."""
        df = pd.DataFrame({"month": ["Jan", "Feb"], "p1": [100, 150], "p2": [200, 180]})
        result = transformer.transform_to_stacked_bar_chart(
            df, "month", ["p1", "p2"], category_names=["Product 1", "Product 2"]
        )

        assert result["categories"] == ["Product 1", "Product 2"]

    def test_stacked_bar_mismatched_names(self, transformer):
        """Test error when category_names count doesn't match."""
        df = pd.DataFrame({"month": ["Jan"], "p1": [100], "p2": [200]})

        with pytest.raises(TransformationError, match="must match"):
            transformer.transform_to_stacked_bar_chart(
                df, "month", ["p1", "p2"], category_names=["Only One"]
            )


class TestDataTable:
    """Tests for transform_to_data_table method."""

    def test_basic_data_table(self, transformer, sample_table_df):
        """Test basic data table transformation."""
        result = transformer.transform_to_data_table(sample_table_df, page=1, page_size=50)

        assert result["chart_type"] == "data_table"
        assert len(result["columns"]) == 3
        assert len(result["rows"]) == 50
        assert result["total"] == 100
        assert result["page"] == 1
        assert result["total_pages"] == 2

    def test_data_table_pagination(self, transformer, sample_table_df):
        """Test data table pagination."""
        result = transformer.transform_to_data_table(sample_table_df, page=2, page_size=25)

        assert len(result["rows"]) == 25
        assert result["page"] == 2
        assert result["rows"][0]["order_id"] == 26

    def test_data_table_column_structure(self, transformer):
        """Test data table column structure."""
        df = pd.DataFrame({"user_id": [1, 2], "user_name": ["Alice", "Bob"]})
        result = transformer.transform_to_data_table(df)

        assert result["columns"][0]["key"] == "user_id"
        assert result["columns"][0]["label"] == "User Id"
        assert result["columns"][1]["key"] == "user_name"
        assert result["columns"][1]["label"] == "User Name"

    def test_data_table_with_nan(self, transformer):
        """Test data table with NaN values."""
        df = pd.DataFrame({"col1": [1, np.nan, 3]})
        result = transformer.transform_to_data_table(df)

        assert result["rows"][1]["col1"] is None


class TestCorrelationHeatmap:
    """Tests for transform_to_correlation_heatmap method."""

    def test_basic_correlation(self, transformer, sample_correlation_df):
        """Test basic correlation heatmap transformation."""
        result = transformer.transform_to_correlation_heatmap(sample_correlation_df)

        assert result["chart_type"] == "heatmap"
        assert len(result["metrics"]) == 3
        assert result["value_label"] == "Correlation Coefficient"
        # Should have 3x3 = 9 data points
        assert len(result["data"]) == 9

    def test_correlation_with_specified_metrics(self, transformer, sample_correlation_df):
        """Test correlation with specified metrics."""
        result = transformer.transform_to_correlation_heatmap(
            sample_correlation_df, metrics=["revenue", "orders"]
        )

        assert len(result["metrics"]) == 2
        assert len(result["data"]) == 4  # 2x2 matrix

    def test_correlation_insufficient_columns(self, transformer):
        """Test error with insufficient numeric columns."""
        df = pd.DataFrame({"col1": [1, 2, 3]})

        with pytest.raises(TransformationError, match="at least 2"):
            transformer.transform_to_correlation_heatmap(df)

    def test_correlation_values(self, transformer):
        """Test that correlation values are reasonable."""
        df = pd.DataFrame(
            {"a": [1, 2, 3, 4, 5], "b": [2, 4, 6, 8, 10]}  # Perfect correlation with 'a'
        )
        result = transformer.transform_to_correlation_heatmap(df)

        # Find correlation between 'a' and 'b'
        ab_corr = next(
            item["value"] for item in result["data"] if item["x"] == "a" and item["y"] == "b"
        )
        # Should be close to 1.0 (perfect positive correlation)
        assert abs(ab_corr - 1.0) < 0.01

    def test_correlation_diagonal_is_one(self, transformer, sample_correlation_df):
        """Test that diagonal values (self-correlation) are 1.0."""
        result = transformer.transform_to_correlation_heatmap(sample_correlation_df)

        diagonal_values = [item["value"] for item in result["data"] if item["x"] == item["y"]]

        for val in diagonal_values:
            assert abs(val - 1.0) < 0.01


class TestExceptionHandling:
    """Tests for exception handling in transformations."""

    def test_transformation_error_attributes(self):
        """Test TransformationError attributes."""
        error = TransformationError(
            "Test error", chart_type="bar_chart", df_shape=(10, 3), missing_columns=["col1", "col2"]
        )

        assert error.message == "Test error"
        assert error.chart_type == "bar_chart"
        assert error.df_shape == (10, 3)
        assert error.missing_columns == ["col1", "col2"]

    def test_transformation_error_string(self):
        """Test TransformationError string representation."""
        error = TransformationError("Test error", chart_type="bar_chart", df_shape=(10, 3))

        error_str = str(error)
        assert "Test error" in error_str
        assert "bar_chart" in error_str
        assert "(10, 3)" in error_str
