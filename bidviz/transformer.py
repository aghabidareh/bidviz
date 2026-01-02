"""
Core chart transformation service - facade for all chart transformers.
"""

from typing import Any, Dict, List, Optional

import pandas as pd

from bidviz.transformers import (
    BarChartTransformer,
    CorrelationHeatmapTransformer,
    DataTableTransformer,
    FunnelChartTransformer,
    HeatmapTransformer,
    KPICardsTransformer,
    LineChartTransformer,
    MultiLineChartTransformer,
    PieChartTransformer,
    StackedBarChartTransformer,
)


class ChartTransformer:
    """
    Main facade for transforming pandas DataFrames into chart-ready data structures.

    This class provides a unified interface to all chart transformers,
    converting raw DataFrames into JSON-serializable formats optimized
    for various charting libraries (Chart.js, D3, Plotly, Recharts, etc.).

    The actual transformation logic is delegated to specialized transformer
    classes for maintainability and modularity.

    Supported chart types:
        - KPI Cards
        - Bar Chart
        - Line Chart
        - Multi-Line Chart
        - Pie Chart
        - Heatmap
        - Funnel Chart
        - Stacked Bar Chart
        - Data Table (with pagination)
        - Correlation Heatmap

    Examples:
        >>> transformer = ChartTransformer()
        >>> df = pd.DataFrame({'vendor': ['A', 'B'], 'revenue': [100, 200]})
        >>> result = transformer.transform_to_bar_chart(df, 'vendor', 'revenue')
        >>> result['chart_type']
        'bar_chart'
    """

    def __init__(self) -> None:
        """Initialize the chart transformer with all specialized transformers."""
        self._kpi_transformer = KPICardsTransformer()
        self._bar_transformer = BarChartTransformer()
        self._line_transformer = LineChartTransformer()
        self._multi_line_transformer = MultiLineChartTransformer()
        self._pie_transformer = PieChartTransformer()
        self._heatmap_transformer = HeatmapTransformer()
        self._funnel_transformer = FunnelChartTransformer()
        self._stacked_bar_transformer = StackedBarChartTransformer()
        self._table_transformer = DataTableTransformer()
        self._correlation_transformer = CorrelationHeatmapTransformer()

    def transform_to_kpi_cards(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Transform a single-row DataFrame into KPI cards for dashboard metrics.

        Args:
            df: Single-row DataFrame containing metrics

        Returns:
            Dict with chart_type='kpi_cards' and list of card data

        Raises:
            TransformationError: If DataFrame has more than one row

        Examples:
            >>> df = pd.DataFrame({'total_orders': [150], 'revenue': [45000.50]})
            >>> result = transformer.transform_to_kpi_cards(df)
            >>> len(result['data'])
            2
        """
        return self._kpi_transformer.transform(df)

    def transform_to_bar_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        label_column: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into bar chart data structure.

        Args:
            df: DataFrame containing the data
            x_column: Column name for x-axis (categorical)
            y_column: Column name for y-axis (numeric)
            label_column: Optional column for custom labels

        Returns:
            Dict with chart_type='bar_chart', data points, and axis labels

        Examples:
            >>> df = pd.DataFrame({'vendor': ['A', 'B'], 'revenue': [1000, 1500]})
            >>> result = transformer.transform_to_bar_chart(df, 'vendor', 'revenue')
            >>> result['chart_type']
            'bar_chart'
        """
        return self._bar_transformer.transform(df, x_column, y_column, label_column)

    def transform_to_line_chart(
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

        Examples:
            >>> df = pd.DataFrame({'date': pd.date_range('2024-01-01', periods=3),
            ...                    'orders': [10, 15, 12]})
            >>> result = transformer.transform_to_line_chart(df, 'date', 'orders')
            >>> result['series_name']
            'Orders'
        """
        return self._line_transformer.transform(df, x_column, y_column, series_name)

    def transform_to_multi_line_chart(
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

        Examples:
            >>> df = pd.DataFrame({'date': ['2024-01-01', '2024-01-02'],
            ...                    'vendor_a': [10, 15], 'vendor_b': [12, 18]})
            >>> result = transformer.transform_to_multi_line_chart(
            ...     df, 'date', ['vendor_a', 'vendor_b'])
            >>> len(result['series'])
            2
        """
        return self._multi_line_transformer.transform(df, x_column, y_columns, series_names)

    def transform_to_pie_chart(
        self, df: pd.DataFrame, label_column: str, value_column: str
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into pie chart data for part-to-whole relationships.

        Args:
            df: DataFrame containing the data
            label_column: Column name for slice labels
            value_column: Column name for slice values

        Returns:
            Dict with chart_type='pie_chart' and data points

        Examples:
            >>> df = pd.DataFrame({'category': ['A', 'B'], 'sales': [45000, 32000]})
            >>> result = transformer.transform_to_pie_chart(df, 'category', 'sales')
            >>> len(result['data'])
            2
        """
        return self._pie_transformer.transform(df, label_column, value_column)

    def transform_to_heatmap(
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

        Examples:
            >>> df = pd.DataFrame({'hour': [0, 1], 'day': ['Mon', 'Mon'],
            ...                    'count': [12, 8]})
            >>> result = transformer.transform_to_heatmap(df, 'hour', 'day', 'count')
            >>> result['chart_type']
            'heatmap'
        """
        return self._heatmap_transformer.transform(df, x_column, y_column, value_column)

    def transform_to_funnel_chart(
        self, df: pd.DataFrame, stage_column: str, value_column: str
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into funnel chart data for conversion pipelines.

        Args:
            df: DataFrame containing the data
            stage_column: Column name for funnel stages
            value_column: Column name for stage values

        Returns:
            Dict with chart_type='funnel_chart' and data points

        Examples:
            >>> df = pd.DataFrame({'stage': ['Visits', 'Sign-ups'],
            ...                    'count': [1000, 300]})
            >>> result = transformer.transform_to_funnel_chart(df, 'stage', 'count')
            >>> len(result['data'])
            2
        """
        return self._funnel_transformer.transform(df, stage_column, value_column)

    def transform_to_stacked_bar_chart(
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

        Examples:
            >>> df = pd.DataFrame({'month': ['Jan', 'Feb'],
            ...                    'product_a': [100, 150], 'product_b': [200, 180]})
            >>> result = transformer.transform_to_stacked_bar_chart(
            ...     df, 'month', ['product_a', 'product_b'])
            >>> len(result['categories'])
            2
        """
        return self._stacked_bar_transformer.transform(df, x_column, y_columns, category_names)

    def transform_to_data_table(
        self, df: pd.DataFrame, page: int = 1, page_size: int = 50
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into paginated data table structure.

        Args:
            df: DataFrame containing the data
            page: Page number (1-indexed)
            page_size: Number of rows per page

        Returns:
            Dict with chart_type='data_table', columns, rows, and pagination

        Examples:
            >>> df = pd.DataFrame({'id': [1, 2, 3], 'name': ['A', 'B', 'C']})
            >>> result = transformer.transform_to_data_table(df, page=1, page_size=2)
            >>> len(result['rows'])
            2
        """
        return self._table_transformer.transform(df, page, page_size)

    def transform_to_correlation_heatmap(
        self, df: pd.DataFrame, metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into correlation heatmap for statistical analysis.

        Args:
            df: DataFrame containing numeric columns
            metrics: Optional list of column names to correlate

        Returns:
            Dict with chart_type='heatmap' and correlation data

        Examples:
            >>> df = pd.DataFrame({'revenue': [100, 200, 150],
            ...                    'orders': [10, 20, 15]})
            >>> result = transformer.transform_to_correlation_heatmap(df)
            >>> result['chart_type']
            'heatmap'
        """
        return self._correlation_transformer.transform(df, metrics)
