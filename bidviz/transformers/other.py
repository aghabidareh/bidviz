"""Funnel and stacked bar chart transformers."""

from typing import Any, Dict, List, Optional

import pandas as pd

from bidviz.core.base import BaseChartTransformer
from bidviz.exceptions import TransformationError
from bidviz.utils import format_label, safe_get_value, validate_columns


class FunnelChartTransformer(BaseChartTransformer):
    """Transform DataFrame into funnel chart data."""

    def transform(self, df: pd.DataFrame, stage_column: str, value_column: str) -> Dict[str, Any]:
        """
        Transform DataFrame into funnel chart data for conversion pipelines.

        Args:
            df: DataFrame containing the data
            stage_column: Column name for funnel stages
            value_column: Column name for stage values

        Returns:
            Dict with chart_type='funnel_chart' and data points
        """
        try:
            validate_columns(df, [stage_column, value_column])

            data = []
            for _, row in df.iterrows():
                data.append(
                    {
                        "stage": str(safe_get_value(row[stage_column])),
                        "value": safe_get_value(row[value_column]),
                    }
                )

            return {"chart_type": "funnel_chart", "data": data}

        except ValueError as e:
            raise TransformationError(str(e), chart_type="funnel_chart", df_shape=df.shape)
        except Exception as e:
            raise TransformationError(
                f"Failed to transform funnel chart: {str(e)}",
                chart_type="funnel_chart",
                df_shape=df.shape,
            )


class StackedBarChartTransformer(BaseChartTransformer):
    """Transform DataFrame into stacked bar chart data."""

    def transform(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_columns: List[str],
        category_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into stacked bar chart for composed comparisons.

        Args:
            df: DataFrame containing the data
            x_column: Column name for x-axis
            y_columns: List of column names for stacked values
            category_names: Optional custom names for each stack

        Returns:
            Dict with chart_type='stacked_bar_chart' and data
        """
        try:
            validate_columns(df, [x_column] + y_columns)

            if category_names and len(category_names) != len(y_columns):
                raise TransformationError(
                    "Number of category_names must match number of y_columns",
                    chart_type="stacked_bar_chart",
                )

            data = []
            for _, row in df.iterrows():
                point = {"x": str(safe_get_value(row[x_column]))}
                for y_col in y_columns:
                    point[y_col] = safe_get_value(row[y_col])
                data.append(point)

            categories = [
                category_names[i] if category_names else format_label(y_col)
                for i, y_col in enumerate(y_columns)
            ]

            return {
                "chart_type": "stacked_bar_chart",
                "data": data,
                "categories": categories,
                "x_label": format_label(x_column),
            }

        except ValueError as e:
            raise TransformationError(str(e), chart_type="stacked_bar_chart", df_shape=df.shape)
        except Exception as e:
            raise TransformationError(
                f"Failed to transform stacked bar chart: {str(e)}",
                chart_type="stacked_bar_chart",
                df_shape=df.shape,
            )
