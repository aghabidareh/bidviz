"""
Utility functions for Polars data transformation and formatting.

These utilities handle Polars-specific data types and conversions,
leveraging Polars' high-performance API for data manipulation.
"""

from typing import Any, List

import polars as pl


def safe_get_value(value: Any) -> Any:
    """
    Safely extract a value from Polars objects, converting null to None.

    Args:
        value: Value to extract (can be Polars type or Python type)

    Returns:
        Python-native value with null converted to None

    Examples:
        >>> safe_get_value(None)
        None
        >>> safe_get_value(42)
        42
        >>> safe_get_value(3.14)
        3.14
    """
    if value is None:
        return None
    if isinstance(value, (int, float, str, bool)):
        return value
    # Handle Polars temporal types
    if hasattr(value, "isoformat"):  # datetime/date/time objects
        return str(value)
    return value


def format_label(column_name: str) -> str:
    """
    Convert snake_case column name to Title Case label.

    Args:
        column_name: Column name in snake_case format

    Returns:
        Formatted label in Title Case

    Examples:
        >>> format_label('total_gmv')
        'Total Gmv'
        >>> format_label('customer_id')
        'Customer Id'
        >>> format_label('avg_days_to_ship')
        'Avg Days To Ship'
    """
    return column_name.replace("_", " ").title()


def validate_columns(df: pl.DataFrame, required_columns: List[str]) -> None:
    """
    Validate that required columns exist in the Polars DataFrame.

    Args:
        df: Polars DataFrame to validate
        required_columns: List of required column names

    Raises:
        ValueError: If any required columns are missing

    Examples:
        >>> df = pl.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> validate_columns(df, ['a', 'b'])  # No error
        >>> validate_columns(df, ['a', 'c'])  # Raises ValueError
        Traceback (most recent call last):
        ...
        ValueError: Missing required columns: c
    """
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def safe_convert_to_numeric(series: pl.Series) -> pl.Series:
    """
    Safely convert a Polars Series to numeric type.

    Args:
        series: Series to convert

    Returns:
        Numeric series with errors converted to null

    Examples:
        >>> s = pl.Series(['1', '2', 'abc'])
        >>> result = safe_convert_to_numeric(s)
        >>> result.to_list()
        [1.0, 2.0, None]
    """
    try:
        return series.cast(pl.Float64, strict=False)
    except Exception:
        return series


def clean_dataframe(df: pl.DataFrame) -> pl.DataFrame:
    """
    Clean DataFrame column names by converting to lowercase and replacing spaces.

    Args:
        df: Polars DataFrame to clean

    Returns:
        DataFrame with cleaned column names

    Examples:
        >>> df = pl.DataFrame({'Total GMV': [100], 'Customer Name': ['John']})
        >>> clean_df = clean_dataframe(df)
        >>> clean_df.columns
        ['total_gmv', 'customer_name']
    """
    new_columns = [col.lower().replace(" ", "_") for col in df.columns]
    return df.rename(dict(zip(df.columns, new_columns)))


def get_numeric_columns(df: pl.DataFrame) -> List[str]:
    """
    Get list of numeric column names from Polars DataFrame.

    Args:
        df: Polars DataFrame to analyze

    Returns:
        List of numeric column names

    Examples:
        >>> df = pl.DataFrame({'a': [1, 2], 'b': ['x', 'y'], 'c': [1.5, 2.5]})
        >>> get_numeric_columns(df)
        ['a', 'c']
    """
    numeric_types = [
        pl.Int8,
        pl.Int16,
        pl.Int32,
        pl.Int64,
        pl.UInt8,
        pl.UInt16,
        pl.UInt32,
        pl.UInt64,
        pl.Float32,
        pl.Float64,
    ]
    return [col for col in df.columns if df[col].dtype in numeric_types]


def paginate_dataframe(
    df: pl.DataFrame, page: int = 1, page_size: int = 50
) -> tuple[pl.DataFrame, dict]:
    """
    Paginate a Polars DataFrame and return pagination metadata.

    Args:
        df: Polars DataFrame to paginate
        page: Page number (1-indexed)
        page_size: Number of rows per page

    Returns:
        Tuple of (paginated DataFrame, pagination metadata dict)

    Examples:
        >>> df = pl.DataFrame({'a': range(100)})
        >>> page_df, meta = paginate_dataframe(df, page=2, page_size=25)
        >>> len(page_df)
        25
        >>> meta['total']
        100
        >>> meta['page']
        2
    """
    total = len(df)
    total_pages = (total + page_size - 1) // page_size  # Ceiling division

    # Ensure page is within valid range
    page = max(1, min(page, total_pages if total_pages > 0 else 1))

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    paginated_df = df.slice(start_idx, page_size)

    metadata = {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }

    return paginated_df, metadata


def dataframe_to_dicts(df: pl.DataFrame) -> List[dict]:
    """
    Convert Polars DataFrame to list of dictionaries with safe value conversion.

    This function handles null values and Polars-specific types properly.

    Args:
        df: Polars DataFrame to convert

    Returns:
        List of dictionaries representing rows

    Examples:
        >>> df = pl.DataFrame({'a': [1, 2], 'b': ['x', 'y']})
        >>> dataframe_to_dicts(df)
        [{'a': 1, 'b': 'x'}, {'a': 2, 'b': 'y'}]
    """
    return [{k: safe_get_value(v) for k, v in row.items()} for row in df.iter_rows(named=True)]
