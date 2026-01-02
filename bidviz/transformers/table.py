"""Data table transformer."""

from typing import Any, Dict

import pandas as pd

from bidviz.core.base import BaseChartTransformer
from bidviz.exceptions import TransformationError
from bidviz.utils import format_label, paginate_dataframe, safe_get_value


class DataTableTransformer(BaseChartTransformer):
    """Transform DataFrame into paginated data table."""

    def transform(self, df: pd.DataFrame, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        """
        Transform DataFrame into paginated data table structure.

        Args:
            df: DataFrame containing the data
            page: Page number (1-indexed)
            page_size: Number of rows per page

        Returns:
            Dict with chart_type='data_table', columns, rows, and pagination
        """
        try:
            paginated_df, metadata = paginate_dataframe(df, page, page_size)

            columns = []
            for col in df.columns:
                columns.append({"key": col, "label": format_label(col)})

            rows = []
            for _, row in paginated_df.iterrows():
                row_data = {}
                for col in df.columns:
                    row_data[col] = safe_get_value(row[col])
                rows.append(row_data)

            return {"chart_type": "data_table", "columns": columns, "rows": rows, **metadata}

        except Exception as e:
            raise TransformationError(
                f"Failed to transform data table: {str(e)}",
                chart_type="data_table",
                df_shape=df.shape,
            )
