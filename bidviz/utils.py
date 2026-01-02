"""
Utility functions for data transformation and formatting.
"""

from typing import Any, List, Optional

import numpy as np
import pandas as pd


def safe_get_value(value: Any) -> Any:
    """
    Safely extract a value from pandas objects, converting NaN to None.

    Args:
        value: Value to extract (can be pandas scalar, numpy type, or Python type)

    Returns:
        Python-native value with NaN converted to None

    Examples:
        >>> safe_get_value(pd.NA)
        None
        >>> safe_get_value(np.nan)
        None
        >>> safe_get_value(42)
        42
    """
    if pd.isna(value):
        return None
    if isinstance(value, (np.integer, np.floating)):
        return float(value) if isinstance(value, np.floating) else int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, (pd.Timestamp, np.datetime64)):
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


def validate_columns(df: pd.DataFrame, required_columns: List[str]) -> None:
    """
    Validate that required columns exist in the DataFrame.

    Args:
        df: DataFrame to validate
        required_columns: List of required column names

    Raises:
        ValueError: If any required columns are missing

    Examples:
        >>> df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        >>> validate_columns(df, ['a', 'b'])  # No error
        >>> validate_columns(df, ['a', 'c'])  # Raises ValueError
        Traceback (most recent call last):
        ...
        ValueError: Missing required columns: c
    """
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")


def safe_convert_to_numeric(series: pd.Series) -> pd.Series:
    """
    Safely convert a pandas Series to numeric type.

    Args:
        series: Series to convert

    Returns:
        Numeric series with errors coerced to NaN

    Examples:
        >>> s = pd.Series(['1', '2', 'abc'])
        >>> safe_convert_to_numeric(s)
        0    1.0
        1    2.0
        2    NaN
        dtype: float64
    """
    return pd.to_numeric(series, errors="coerce")


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean DataFrame column names by converting to lowercase and replacing spaces.

    Args:
        df: DataFrame to clean

    Returns:
        DataFrame with cleaned column names

    Examples:
        >>> df = pd.DataFrame({'Total GMV': [100], 'Customer Name': ['John']})
        >>> clean_df = clean_dataframe(df)
        >>> list(clean_df.columns)
        ['total_gmv', 'customer_name']
    """
    df = df.copy()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """
    Get list of numeric column names from DataFrame.

    Args:
        df: DataFrame to analyze

    Returns:
        List of numeric column names

    Examples:
        >>> df = pd.DataFrame({'a': [1, 2], 'b': ['x', 'y'], 'c': [1.5, 2.5]})
        >>> get_numeric_columns(df)
        ['a', 'c']
    """
    return df.select_dtypes(include=[np.number]).columns.tolist()


def paginate_dataframe(
    df: pd.DataFrame, page: int = 1, page_size: int = 50
) -> tuple[pd.DataFrame, dict]:
    """
    Paginate a DataFrame and return pagination metadata.

    Args:
        df: DataFrame to paginate
        page: Page number (1-indexed)
        page_size: Number of rows per page

    Returns:
        Tuple of (paginated DataFrame, pagination metadata dict)

    Examples:
        >>> df = pd.DataFrame({'a': range(100)})
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

    paginated_df = df.iloc[start_idx:end_idx]

    metadata = {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }

    return paginated_df, metadata
