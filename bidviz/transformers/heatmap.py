"""Heatmap transformers."""

from typing import Any, Dict, List, Optional

import pandas as pd

from bidviz.core.base import BaseChartTransformer
from bidviz.exceptions import TransformationError
from bidviz.utils import format_label, get_numeric_columns, safe_get_value, validate_columns


class HeatmapTransformer(BaseChartTransformer):
    """Transform DataFrame into heatmap data."""

    def transform(
        self, df: pd.DataFrame, x_column: str, y_column: str, value_column: str
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into heatmap data for 2D intensity visualization.

        Args:
            df: DataFrame containing the data
            x_column: Column name for x-axis
            y_column: Column name for y-axis
            value_column: Column name for cell values

        Returns:
            Dict with chart_type='heatmap', data points, and labels
        """
        try:
            validate_columns(df, [x_column, y_column, value_column])

            data = []
            for _, row in df.iterrows():
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
    """Transform DataFrame into correlation heatmap."""

    def transform(self, df: pd.DataFrame, metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Transform DataFrame into correlation heatmap for statistical analysis.

        Args:
            df: DataFrame containing numeric columns
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
            corr_matrix = df[metrics].corr()

            data = []
            for x_metric in metrics:
                for y_metric in metrics:
                    data.append(
                        {
                            "x": x_metric,
                            "y": y_metric,
                            "value": safe_get_value(corr_matrix.loc[y_metric, x_metric]),
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
