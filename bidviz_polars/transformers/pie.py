"""Pie chart transformer for Polars DataFrames."""

from typing import Any, Dict

import polars as pl

from bidviz.exceptions import TransformationError
from bidviz_polars.core.base import BaseChartTransformer
from bidviz_polars.utils import format_label, safe_get_value, validate_columns


class PieChartTransformer(BaseChartTransformer):
    """Transform Polars DataFrame into pie chart data."""

    def transform(
        self, df: pl.DataFrame, label_column: str, value_column: str
    ) -> Dict[str, Any]:
        """
        Transform Polars DataFrame into pie chart data for part-to-whole relationships.

        Args:
            df: Polars DataFrame containing the data
            label_column: Column name for slice labels
            value_column: Column name for slice values

        Returns:
            Dict with chart_type='pie_chart' and data points

        Raises:
            TransformationError: If required columns are missing
        """
        try:
            validate_columns(df, [label_column, value_column])

            data = []
            for row in df.iter_rows(named=True):
                data.append(
                    {
                        "label": str(safe_get_value(row[label_column])),
                        "value": safe_get_value(row[value_column]),
                    }
                )

            return {
                "chart_type": "pie_chart",
                "data": data,
                "label": format_label(label_column),
            }

        except ValueError as e:
            raise TransformationError(str(e), chart_type="pie_chart", df_shape=df.shape)
        except Exception as e:
            raise TransformationError(
                f"Failed to transform pie chart: {str(e)}",
                chart_type="pie_chart",
                df_shape=df.shape,
            )
