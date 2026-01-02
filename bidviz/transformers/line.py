"""Line chart transformers."""

from typing import Any, Dict, List, Optional

import pandas as pd

from bidviz.core.base import BaseChartTransformer
from bidviz.exceptions import TransformationError
from bidviz.utils import format_label, safe_get_value, validate_columns


class LineChartTransformer(BaseChartTransformer):
    """Transform DataFrame into line chart data."""

    def transform(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        series_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into line chart data for time series or trends.

        Args:
            df: DataFrame containing the data
            x_column: Column name for x-axis
            y_column: Column name for y-axis
            series_name: Optional custom name for the data series

        Returns:
            Dict with chart_type='line_chart', data points, and labels
        """
        try:
            validate_columns(df, [x_column, y_column])

            data = []
            for _, row in df.iterrows():
                data.append(
                    {
                        "x": str(safe_get_value(row[x_column])),
                        "y": safe_get_value(row[y_column]),
                    }
                )

            return {
                "chart_type": "line_chart",
                "data": data,
                "series_name": series_name or format_label(y_column),
                "x_label": format_label(x_column),
                "y_label": format_label(y_column),
            }

        except ValueError as e:
            raise TransformationError(str(e), chart_type="line_chart", df_shape=df.shape)
        except Exception as e:
            raise TransformationError(
                f"Failed to transform line chart: {str(e)}",
                chart_type="line_chart",
                df_shape=df.shape,
            )


class MultiLineChartTransformer(BaseChartTransformer):
    """Transform DataFrame into multi-line chart data."""

    def transform(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_columns: List[str],
        series_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into multi-line chart for comparing multiple series.

        Args:
            df: DataFrame containing the data
            x_column: Column name for x-axis
            y_columns: List of column names for y-axis
            series_names: Optional custom names for each series

        Returns:
            Dict with chart_type='multi_line_chart' and series data
        """
        try:
            validate_columns(df, [x_column] + y_columns)

            if series_names and len(series_names) != len(y_columns):
                raise TransformationError(
                    "Number of series_names must match number of y_columns",
                    chart_type="multi_line_chart",
                )

            series = []
            for idx, y_col in enumerate(y_columns):
                data = []
                for _, row in df.iterrows():
                    data.append(
                        {
                            "x": str(safe_get_value(row[x_column])),
                            "y": safe_get_value(row[y_col]),
                        }
                    )

                series.append(
                    {
                        "name": series_names[idx] if series_names else format_label(y_col),
                        "data": data,
                    }
                )

            return {
                "chart_type": "multi_line_chart",
                "series": series,
                "x_label": format_label(x_column),
            }

        except ValueError as e:
            raise TransformationError(str(e), chart_type="multi_line_chart", df_shape=df.shape)
        except Exception as e:
            raise TransformationError(
                f"Failed to transform multi-line chart: {str(e)}",
                chart_type="multi_line_chart",
                df_shape=df.shape,
            )
