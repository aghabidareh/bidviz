"""Base transformer class for all chart transformations."""

from typing import Any, Dict

import pandas as pd


class BaseChartTransformer:
    """
    Base class for chart transformers.

    All specific chart transformers should inherit from this class
    and implement the transform method.
    """

    def transform(self, df: pd.DataFrame, **kwargs: Any) -> Dict[str, Any]:
        """
        Transform a DataFrame into chart-ready format.

        Args:
            df: Input DataFrame
            **kwargs: Additional transformation parameters

        Returns:
            Dictionary containing chart data and metadata

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement transform method")

    def _validate_dataframe(self, df: pd.DataFrame) -> None:
        """
        Validate that DataFrame is not None and has data.

        Args:
            df: DataFrame to validate

        Raises:
            ValueError: If DataFrame is None
        """
        if df is None:
            raise ValueError("DataFrame cannot be None")
