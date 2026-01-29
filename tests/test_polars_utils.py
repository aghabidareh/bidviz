"""Tests for Polars utility functions."""

import polars as pl
import pytest

from bidviz_polars import (
    clean_dataframe,
    dataframe_to_dicts,
    format_label,
    get_numeric_columns,
    paginate_dataframe,
    safe_convert_to_numeric,
    safe_get_value,
    validate_columns,
)


class TestSafeGetValue:
    """Tests for safe_get_value function."""

    def test_none_value(self):
        """Test that None is preserved."""
        assert safe_get_value(None) is None

    def test_regular_integer(self):
        """Test that regular integers are preserved."""
        assert safe_get_value(42) == 42

    def test_regular_float(self):
        """Test that regular floats are preserved."""
        assert safe_get_value(3.14) == 3.14

    def test_string_value(self):
        """Test that strings are preserved."""
        assert safe_get_value("hello") == "hello"

    def test_boolean_value(self):
        """Test that boolean values are preserved."""
        assert safe_get_value(True) is True
        assert safe_get_value(False) is False


class TestFormatLabel:
    """Tests for format_label function."""

    def test_basic_snake_case(self):
        """Test basic snake_case conversion."""
        assert format_label("total_gmv") == "Total Gmv"

    def test_multiple_underscores(self):
        """Test multiple underscores."""
        assert format_label("avg_days_to_ship") == "Avg Days To Ship"

    def test_single_word(self):
        """Test single word without underscores."""
        assert format_label("revenue") == "Revenue"

    def test_with_numbers(self):
        """Test with numbers in the name."""
        assert format_label("customer_id") == "Customer Id"

    def test_empty_string(self):
        """Test with empty string."""
        assert format_label("") == ""


class TestValidateColumns:
    """Tests for validate_columns function."""

    def test_all_columns_present(self):
        """Test when all required columns are present."""
        df = pl.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]})
        validate_columns(df, ["a", "b"])  # Should not raise

    def test_single_column_present(self):
        """Test when single required column is present."""
        df = pl.DataFrame({"a": [1, 2]})
        validate_columns(df, ["a"])  # Should not raise

    def test_missing_single_column(self):
        """Test when a single column is missing."""
        df = pl.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="Missing required columns: b"):
            validate_columns(df, ["a", "b"])

    def test_missing_multiple_columns(self):
        """Test when multiple columns are missing."""
        df = pl.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="Missing required columns"):
            validate_columns(df, ["b", "c"])


class TestSafeConvertToNumeric:
    """Tests for safe_convert_to_numeric function."""

    def test_string_numbers(self):
        """Test converting string numbers."""
        s = pl.Series(["1", "2", "3"])
        result = safe_convert_to_numeric(s)
        assert result.dtype == pl.Float64
        assert result.to_list() == [1.0, 2.0, 3.0]

    def test_mixed_with_non_numeric(self):
        """Test converting mixed strings with non-numeric values."""
        s = pl.Series(["1", "2", "abc"])
        result = safe_convert_to_numeric(s)
        values = result.to_list()
        assert values[0] == 1.0
        assert values[1] == 2.0
        assert values[2] is None


class TestCleanDataframe:
    """Tests for clean_dataframe function."""

    def test_basic_cleaning(self):
        """Test basic column name cleaning."""
        df = pl.DataFrame({"Total GMV": [100], "Customer Name": ["John"]})
        result = clean_dataframe(df)
        assert result.columns == ["total_gmv", "customer_name"]

    def test_already_clean(self):
        """Test with already clean column names."""
        df = pl.DataFrame({"total_gmv": [100]})
        result = clean_dataframe(df)
        assert result.columns == ["total_gmv"]

    def test_multiple_spaces(self):
        """Test with multiple spaces in column names."""
        df = pl.DataFrame({"Total  Revenue": [100]})
        result = clean_dataframe(df)
        assert result.columns == ["total__revenue"]


class TestGetNumericColumns:
    """Tests for get_numeric_columns function."""

    def test_all_numeric(self):
        """Test when all columns are numeric."""
        df = pl.DataFrame({"a": [1, 2], "b": [3.5, 4.5]})
        result = get_numeric_columns(df)
        assert set(result) == {"a", "b"}

    def test_mixed_types(self):
        """Test with mixed column types."""
        df = pl.DataFrame({"a": [1, 2], "b": ["x", "y"], "c": [1.5, 2.5]})
        result = get_numeric_columns(df)
        assert set(result) == {"a", "c"}

    def test_no_numeric(self):
        """Test when no columns are numeric."""
        df = pl.DataFrame({"a": ["x", "y"], "b": ["z", "w"]})
        result = get_numeric_columns(df)
        assert result == []


class TestPaginateDataframe:
    """Tests for paginate_dataframe function."""

    def test_basic_pagination(self):
        """Test basic pagination."""
        df = pl.DataFrame({"a": list(range(100))})
        result_df, metadata = paginate_dataframe(df, page=1, page_size=25)

        assert len(result_df) == 25
        assert metadata["total"] == 100
        assert metadata["page"] == 1
        assert metadata["page_size"] == 25
        assert metadata["total_pages"] == 4

    def test_second_page(self):
        """Test getting second page."""
        df = pl.DataFrame({"a": list(range(100))})
        result_df, metadata = paginate_dataframe(df, page=2, page_size=25)

        assert len(result_df) == 25
        assert result_df["a"][0] == 25  # First item of second page

    def test_last_page_partial(self):
        """Test last page with partial results."""
        df = pl.DataFrame({"a": list(range(55))})
        result_df, metadata = paginate_dataframe(df, page=3, page_size=25)

        assert len(result_df) == 5  # Remaining items
        assert metadata["total_pages"] == 3

    def test_page_beyond_range(self):
        """Test requesting page beyond available pages."""
        df = pl.DataFrame({"a": list(range(10))})
        result_df, metadata = paginate_dataframe(df, page=10, page_size=25)

        # Should return empty but valid response
        assert metadata["page"] == 1  # Clamped to valid range

    def test_empty_dataframe(self):
        """Test pagination with empty DataFrame."""
        df = pl.DataFrame({"a": []})
        result_df, metadata = paginate_dataframe(df, page=1, page_size=25)

        assert len(result_df) == 0
        assert metadata["total"] == 0
        assert metadata["total_pages"] == 0


class TestDataframeToDicts:
    """Tests for dataframe_to_dicts function."""

    def test_basic_conversion(self):
        """Test basic DataFrame to dict conversion."""
        df = pl.DataFrame({"a": [1, 2], "b": ["x", "y"]})
        result = dataframe_to_dicts(df)

        assert len(result) == 2
        assert result[0] == {"a": 1, "b": "x"}
        assert result[1] == {"a": 2, "b": "y"}

    def test_with_null_values(self):
        """Test conversion with null values."""
        df = pl.DataFrame({"a": [1, None], "b": ["x", "y"]})
        result = dataframe_to_dicts(df)

        assert result[0]["a"] == 1
        assert result[1]["a"] is None

    def test_empty_dataframe(self):
        """Test conversion of empty DataFrame."""
        df = pl.DataFrame({"a": [], "b": []})
        result = dataframe_to_dicts(df)

        assert result == []
