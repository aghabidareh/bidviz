"""Pie and donut chart transformers."""

from typing import Any, Dict

import pandas as pd

from bidviz.core.base import BaseChartTransformer
from bidviz.exceptions import TransformationError
from bidviz.utils import safe_get_value, validate_columns


class PieChartTransformer(BaseChartTransformer):
    """Transform DataFrame into pie chart data."""

    def transform(self, df: pd.DataFrame, label_column: str, value_column: str) -> Dict[str, Any]:
        """
        Transform DataFrame into pie chart data for part-to-whole relationships.

        Args:
            df: DataFrame containing the data
            label_column: Column name for slice labels
            value_column: Column name for slice values

        Returns:
            Dict with chart_type='pie_chart' and data points
        """
        try:
            validate_columns(df, [label_column, value_column])

            data = []
            for _, row in df.iterrows():
                data.append(
                    {
                        "label": str(safe_get_value(row[label_column])),
                        "value": safe_get_value(row[value_column]),
                    }
                )

            return {"chart_type": "pie_chart", "data": data}

        except ValueError as e:
            raise TransformationError(str(e), chart_type="pie_chart", df_shape=df.shape)
        except Exception as e:
            raise TransformationError(
                f"Failed to transform pie chart: {str(e)}",
                chart_type="pie_chart",
                df_shape=df.shape,
            )
