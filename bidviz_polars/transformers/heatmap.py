"""Heatmap transformers for Polars DataFrames."""

from typing import Any, Dict, List, Optional

import polars as pl

from bidviz.exceptions import TransformationError
from bidviz_polars.core.base import BaseChartTransformer
from bidviz_polars.utils import format_label, get_numeric_columns, safe_get_value, validate_columns


class HeatmapTransformer(BaseChartTransformer):
    """Transform Polars DataFrame into heatmap data."""

    def transform(
        self, df: pl.DataFrame, x_column: str, y_column: str, value_column: str
    ) -> Dict[str, Any]:
        """
        Transform Polars DataFrame into heatmap data for 2D intensity visualization.

        Args:
            df: Polars DataFrame containing the data
            x_column: Column name for x-axis
            y_column: Column name for y-axis
            value_column: Column name for cell values

        Returns:
            Dict with chart_type='heatmap', data points, and labels
        """
        try:
            validate_columns(df, [x_column, y_column, value_column])

            data = []
            for row in df.iter_rows(named=True):
                data.append(
                    {
                        "x": str(safe_get_value(row[x_column])),
                        "y": str(safe_get_value(row[y_column])),
                        "value": safe_get_value(row[value_column]),
                    }
                )

            return {
                "chart_type": "heatmap",
                "data": data,
                "x_label": format_label(x_column),
                "y_label": format_label(y_column),
                "value_label": format_label(value_column),
            }

        except ValueError as e:
            raise TransformationError(str(e), chart_type="heatmap", df_shape=df.shape)
        except Exception as e:
            raise TransformationError(
                f"Failed to transform heatmap: {str(e)}",
                chart_type="heatmap",
                df_shape=df.shape,
            )


class CorrelationHeatmapTransformer(BaseChartTransformer):
    """Transform Polars DataFrame into correlation heatmap."""

    def transform(self, df: pl.DataFrame, metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Transform Polars DataFrame into correlation heatmap for statistical analysis.

        Args:
            df: Polars DataFrame containing numeric columns
            metrics: Optional list of column names to correlate

        Returns:
            Dict with chart_type='heatmap' and correlation data
        """
        try:
            if metrics is None:
                metrics = get_numeric_columns(df)

            if len(metrics) < 2:
                raise TransformationError(
                    "Need at least 2 numeric columns for correlation",
                    chart_type="correlation_heatmap",
                    df_shape=df.shape,
                )

            validate_columns(df, metrics)

            # Polars uses corr() method on DataFrame
            corr_matrix = df.select(metrics).corr()

            data = []
            for i, x_metric in enumerate(metrics):
                for j, y_metric in enumerate(metrics):
                    # Access correlation value from the matrix
                    value = corr_matrix.row(j)[i]
                    data.append(
                        {
                            "x": x_metric,
                            "y": y_metric,
                            "value": safe_get_value(value),
                        }
                    )

            return {
                "chart_type": "heatmap",
                "data": data,
                "metrics": metrics,
                "x_label": "Metrics",
                "y_label": "Metrics",
                "value_label": "Correlation Coefficient",
            }

        except ValueError as e:
            raise TransformationError(str(e), chart_type="correlation_heatmap", df_shape=df.shape)
        except Exception as e:
            raise TransformationError(
                f"Failed to transform correlation heatmap: {str(e)}",
                chart_type="correlation_heatmap",
                df_shape=df.shape,
            )
