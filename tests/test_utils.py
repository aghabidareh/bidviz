"""Tests for utility functions."""

import numpy as np
import pandas as pd
import pytest

from bidviz.utils import (
    clean_dataframe,
    format_label,
    get_numeric_columns,
    paginate_dataframe,
    safe_convert_to_numeric,
    safe_get_value,
    validate_columns,
)


class TestSafeGetValue:
    """Tests for safe_get_value function."""

    def test_none_from_pandas_na(self):
        """Test that pandas NA is converted to None."""
        assert safe_get_value(pd.NA) is None

    def test_none_from_numpy_nan(self):
        """Test that numpy NaN is converted to None."""
        assert safe_get_value(np.nan) is None

    def test_regular_integer(self):
        """Test that regular integers are preserved."""
        assert safe_get_value(42) == 42

    def test_regular_float(self):
        """Test that regular floats are preserved."""
        assert safe_get_value(3.14) == 3.14

    def test_numpy_integer(self):
        """Test that numpy integers are converted to Python int."""
        result = safe_get_value(np.int64(42))
        assert result == 42
        assert isinstance(result, int)

    def test_numpy_float(self):
        """Test that numpy floats are converted to Python float."""
        result = safe_get_value(np.float64(3.14))
        assert result == 3.14
        assert isinstance(result, float)

    def test_string_value(self):
        """Test that strings are preserved."""
        assert safe_get_value("hello") == "hello"

    def test_pandas_timestamp(self):
        """Test that pandas timestamps are converted to string."""
        ts = pd.Timestamp("2024-01-01")
        result = safe_get_value(ts)
        assert isinstance(result, str)
        assert "2024-01-01" in result

    def test_boolean_value(self):
        """Test that boolean values are preserved."""
        assert safe_get_value(True) is True
        assert safe_get_value(False) is False

    def test_numpy_bool(self):
        """Test that numpy booleans are converted to Python bool."""
        result = safe_get_value(np.bool_(True))
        assert result is True
        assert isinstance(result, bool)


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
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]})
        validate_columns(df, ["a", "b"])  # Should not raise

    def test_missing_single_column(self):
        """Test when a single column is missing."""
        df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        with pytest.raises(ValueError, match="Missing required columns: c"):
            validate_columns(df, ["a", "c"])

    def test_missing_multiple_columns(self):
        """Test when multiple columns are missing."""
        df = pd.DataFrame({"a": [1, 2]})
        with pytest.raises(ValueError, match="Missing required columns"):
            validate_columns(df, ["b", "c"])

    def test_empty_required_list(self):
        """Test with empty required columns list."""
        df = pd.DataFrame({"a": [1, 2]})
        validate_columns(df, [])  # Should not raise


class TestSafeConvertToNumeric:
    """Tests for safe_convert_to_numeric function."""

    def test_convert_string_numbers(self):
        """Test converting string numbers to numeric."""
        s = pd.Series(["1", "2", "3"])
        result = safe_convert_to_numeric(s)
        assert result.tolist() == [1.0, 2.0, 3.0]

    def test_coerce_non_numeric(self):
        """Test that non-numeric values are coerced to NaN."""
        s = pd.Series(["1", "abc", "3"])
        result = safe_convert_to_numeric(s)
        assert result[0] == 1.0
        assert pd.isna(result[1])
        assert result[2] == 3.0

    def test_already_numeric(self):
        """Test with already numeric series."""
        s = pd.Series([1, 2, 3])
        result = safe_convert_to_numeric(s)
        assert result.tolist() == [1, 2, 3]


class TestCleanDataFrame:
    """Tests for clean_dataframe function."""

    def test_lowercase_conversion(self):
        """Test converting columns to lowercase."""
        df = pd.DataFrame({"TotalGMV": [100], "CustomerName": ["John"]})
        result = clean_dataframe(df)
        assert "totalgmv" in result.columns
        assert "customername" in result.columns

    def test_space_replacement(self):
        """Test replacing spaces with underscores."""
        df = pd.DataFrame({"Total GMV": [100], "Customer Name": ["John"]})
        result = clean_dataframe(df)
        assert "total_gmv" in result.columns
        assert "customer_name" in result.columns

    def test_combined_cleaning(self):
        """Test combined lowercase and space replacement."""
        df = pd.DataFrame({"Total GMV": [100]})
        result = clean_dataframe(df)
        assert list(result.columns) == ["total_gmv"]

    def test_original_df_unchanged(self):
        """Test that original DataFrame is not modified."""
        df = pd.DataFrame({"Total GMV": [100]})
        original_cols = df.columns.tolist()
        clean_dataframe(df)
        assert df.columns.tolist() == original_cols


class TestGetNumericColumns:
    """Tests for get_numeric_columns function."""

    def test_all_numeric(self):
        """Test DataFrame with all numeric columns."""
        df = pd.DataFrame({"a": [1, 2], "b": [3.0, 4.0], "c": [5, 6]})
        result = get_numeric_columns(df)
        assert set(result) == {"a", "b", "c"}

    def test_mixed_types(self):
        """Test DataFrame with mixed types."""
        df = pd.DataFrame({"num1": [1, 2], "text": ["a", "b"], "num2": [3.0, 4.0]})
        result = get_numeric_columns(df)
        assert set(result) == {"num1", "num2"}

    def test_no_numeric(self):
        """Test DataFrame with no numeric columns."""
        df = pd.DataFrame({"text1": ["a", "b"], "text2": ["c", "d"]})
        result = get_numeric_columns(df)
        assert result == []

    def test_empty_dataframe(self):
        """Test empty DataFrame."""
        df = pd.DataFrame()
        result = get_numeric_columns(df)
        assert result == []


class TestPaginateDataFrame:
    """Tests for paginate_dataframe function."""

    def test_first_page(self):
        """Test getting first page."""
        df = pd.DataFrame({"a": range(100)})
        result_df, meta = paginate_dataframe(df, page=1, page_size=25)
        assert len(result_df) == 25
        assert result_df["a"].tolist() == list(range(25))
        assert meta["total"] == 100
        assert meta["page"] == 1
        assert meta["total_pages"] == 4

    def test_middle_page(self):
        """Test getting middle page."""
        df = pd.DataFrame({"a": range(100)})
        result_df, meta = paginate_dataframe(df, page=2, page_size=25)
        assert len(result_df) == 25
        assert result_df["a"].tolist() == list(range(25, 50))

    def test_last_page_partial(self):
        """Test getting last page with partial results."""
        df = pd.DataFrame({"a": range(100)})
        result_df, meta = paginate_dataframe(df, page=3, page_size=40)
        assert len(result_df) == 20
        assert result_df["a"].tolist() == list(range(80, 100))

    def test_page_beyond_total(self):
        """Test requesting page beyond total pages."""
        df = pd.DataFrame({"a": range(10)})
        result_df, meta = paginate_dataframe(df, page=10, page_size=5)
        assert meta["page"] == 2  # Clamped to max page
        assert len(result_df) <= 5

    def test_negative_page(self):
        """Test with negative page number."""
        df = pd.DataFrame({"a": range(50)})
        result_df, meta = paginate_dataframe(df, page=-1, page_size=10)
        assert meta["page"] == 1  # Clamped to minimum

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        df = pd.DataFrame({"a": []})
        result_df, meta = paginate_dataframe(df, page=1, page_size=10)
        assert len(result_df) == 0
        assert meta["total"] == 0
        assert meta["total_pages"] == 0

    def test_custom_page_size(self):
        """Test with custom page size."""
        df = pd.DataFrame({"a": range(100)})
        result_df, meta = paginate_dataframe(df, page=1, page_size=15)
        assert len(result_df) == 15
        assert meta["page_size"] == 15
        assert meta["total_pages"] == 7  # ceil(100/15)
