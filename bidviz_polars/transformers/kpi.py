"""KPI Cards transformer for Polars DataFrames."""

from typing import Any, Dict

import polars as pl

from bidviz.exceptions import TransformationError
from bidviz_polars.core.base import BaseChartTransformer
from bidviz_polars.utils import format_label, safe_get_value


class KPICardsTransformer(BaseChartTransformer):
    """Transform single-row Polars DataFrame into KPI cards."""

    def transform(self, df: pl.DataFrame) -> Dict[str, Any]:
        """
        Transform a single-row Polars DataFrame into KPI cards for dashboard metrics.

        Args:
            df: Single-row Polars DataFrame containing metrics

        Returns:
            Dict with chart_type='kpi_cards' and list of card data

        Raises:
            TransformationError: If DataFrame has more than one row
        """
        try:
            if len(df) == 0:
                return {"chart_type": "kpi_cards", "data": []}

            if len(df) > 1:
                raise TransformationError(
                    "KPI cards expect a single-row DataFrame",
                    chart_type="kpi_cards",
                    df_shape=df.shape,
                )

            row = df.row(0, named=True)
            cards = []

            for column in df.columns:
                cards.append(
                    {
                        "key": column,
                        "label": format_label(column),
                        "value": safe_get_value(row[column]),
                    }
                )

            return {"chart_type": "kpi_cards", "data": cards}

        except Exception as e:
            if isinstance(e, TransformationError):
                raise
            raise TransformationError(
                f"Failed to transform KPI cards: {str(e)}",
                chart_type="kpi_cards",
                df_shape=df.shape,
            )
