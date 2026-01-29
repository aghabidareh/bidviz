"""Bar chart transformer for Polars DataFrames."""

from typing import Any, Dict, Optional

import polars as pl

from bidviz.exceptions import TransformationError
from bidviz_polars.core.base import BaseChartTransformer
from bidviz_polars.utils import format_label, safe_get_value, validate_columns


class BarChartTransformer(BaseChartTransformer):
    """Transform Polars DataFrame into bar chart data."""

    def transform(
        self,
        df: pl.DataFrame,
        x_column: str,
        y_column: str,
        label_column: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transform Polars DataFrame into bar chart data structure.

        Args:
            df: Polars DataFrame containing the data
            x_column: Column name for x-axis (categorical)
            y_column: Column name for y-axis (numeric)
            label_column: Optional column for custom labels

        Returns:
            Dict with chart_type='bar_chart', data points, and axis labels

        Raises:
            TransformationError: If required columns are missing
        """
        try:
            validate_columns(df, [x_column, y_column])
            if label_column:
                validate_columns(df, [label_column])
            else:
                label_column = x_column

            data = []
            for row in df.iter_rows(named=True):
                data.append(
                    {
                        "x": str(safe_get_value(row[x_column])),
                        "y": safe_get_value(row[y_column]),
                        "label": str(safe_get_value(row[label_column])),
                    }
                )

            return {
                "chart_type": "bar_chart",
                "data": data,
                "x_label": format_label(x_column),
                "y_label": format_label(y_column),
            }

        except ValueError as e:
            raise TransformationError(str(e), chart_type="bar_chart", df_shape=df.shape)
        except Exception as e:
            raise TransformationError(
                f"Failed to transform bar chart: {str(e)}",
                chart_type="bar_chart",
                df_shape=df.shape,
            )
