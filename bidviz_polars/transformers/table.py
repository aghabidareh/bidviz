"""Data table transformer for Polars DataFrames."""

from typing import Any, Dict

import polars as pl

from bidviz.exceptions import TransformationError
from bidviz_polars.core.base import BaseChartTransformer
from bidviz_polars.utils import format_label, paginate_dataframe, safe_get_value


class DataTableTransformer(BaseChartTransformer):
    """Transform Polars DataFrame into paginated data table."""

    def transform(self, df: pl.DataFrame, page: int = 1, page_size: int = 50) -> Dict[str, Any]:
        """
        Transform Polars DataFrame into paginated data table structure.

        Args:
            df: Polars DataFrame containing the data
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
            for row in paginated_df.iter_rows(named=True):
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
