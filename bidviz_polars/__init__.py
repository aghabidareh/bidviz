"""
BidViz Polars - High-performance chart data transformation using Polars.

This module provides Polars-based transformers for converting Polars DataFrames
into JSON-serializable formats optimized for frontend charting libraries.

Polars offers superior performance compared to pandas, especially for larger datasets,
with lazy evaluation, parallel processing, and memory efficiency.

Main Classes:
    ChartTransformer: Facade for all Polars-based chart transformations
    TransformationError: Exception for transformation failures
    ValidationError: Exception for validation failures

Example:
    >>> import polars as pl
    >>> from bidviz_polars import ChartTransformer
    >>>
    >>> transformer = ChartTransformer()
    >>> df = pl.DataFrame({'vendor': ['A', 'B'], 'revenue': [100, 200]})
    >>> result = transformer.transform_to_bar_chart(df, 'vendor', 'revenue')
"""

from bidviz.exceptions import TransformationError, ValidationError
from bidviz_polars.transformer import ChartTransformer

__version__ = "1.0.0"

__all__ = [
    "ChartTransformer",
    "TransformationError",
    "ValidationError",
]
