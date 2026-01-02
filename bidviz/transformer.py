"""
Core chart transformation service for converting pandas DataFrames to chart-ready formats.
"""

from typing import Any, Dict, List, Optional

import pandas as pd

from bidviz.exceptions import TransformationError
from bidviz.utils import (
    format_label,
    get_numeric_columns,
    paginate_dataframe,
    safe_get_value,
    validate_columns,
)


class ChartTransformer:
    """
    Main service for transforming pandas DataFrames into frontend-ready chart data structures.

    This class provides methods to convert raw DataFrames into JSON-serializable formats
    optimized for various charting libraries (Chart.js, D3, Plotly, Recharts, etc.).

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
            >>> result['data'][0]['label']
            'Total Orders'
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

            row = df.iloc[0]
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
            label_column: Optional column for custom labels (defaults to x_column)

        Returns:
            Dict with chart_type='bar_chart', data points, and axis labels

        Raises:
            TransformationError: If required columns are missing

        Examples:
            >>> df = pd.DataFrame({
            ...     'vendor': ['A', 'B', 'C'],
            ...     'revenue': [1000, 1500, 1200]
            ... })
            >>> result = transformer.transform_to_bar_chart(df, 'vendor', 'revenue')
            >>> len(result['data'])
            3
            >>> result['x_label']
            'Vendor'
        """
        try:
            validate_columns(df, [x_column, y_column])
            if label_column:
                validate_columns(df, [label_column])
            else:
                label_column = x_column

            data = []
            for _, row in df.iterrows():
                data.append(
                    {
                        "x": str(safe_get_value(row[x_column])),
                        "y": safe_get_value(row[y_column]),
                        "label": str(safe_get_value(row[label_column])),
                    }
                )

            return {
                "chart_type": "bar_chart",
                "data": data,
                "x_label": format_label(x_column),
                "y_label": format_label(y_column),
            }

        except ValueError as e:
            raise TransformationError(str(e), chart_type="bar_chart", df_shape=df.shape)
        except Exception as e:
            raise TransformationError(
                f"Failed to transform bar chart: {str(e)}",
                chart_type="bar_chart",
                df_shape=df.shape,
            )

    def transform_to_line_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        series_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into line chart data structure for time series or trends.

        Args:
            df: DataFrame containing the data
            x_column: Column name for x-axis (typically dates/time)
            y_column: Column name for y-axis (numeric)
            series_name: Optional custom name for the data series

        Returns:
            Dict with chart_type='line_chart', data points, series name, and axis labels

        Raises:
            TransformationError: If required columns are missing

        Examples:
            >>> df = pd.DataFrame({
            ...     'date': pd.date_range('2024-01-01', periods=3),
            ...     'orders': [10, 15, 12]
            ... })
            >>> result = transformer.transform_to_line_chart(df, 'date', 'orders')
            >>> result['series_name']
            'Orders'
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

    def transform_to_multi_line_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_columns: List[str],
        series_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into multi-line chart data for comparing multiple series.

        Args:
            df: DataFrame containing the data
            x_column: Column name for x-axis (shared across all series)
            y_columns: List of column names for y-axis (one per series)
            series_names: Optional custom names for each series

        Returns:
            Dict with chart_type='multi_line_chart', series data, and x-axis label

        Raises:
            TransformationError: If required columns are missing

        Examples:
            >>> df = pd.DataFrame({
            ...     'date': ['2024-01-01', '2024-01-02'],
            ...     'vendor_a': [10, 15],
            ...     'vendor_b': [12, 18]
            ... })
            >>> result = transformer.transform_to_multi_line_chart(
            ...     df, 'date', ['vendor_a', 'vendor_b']
            ... )
            >>> len(result['series'])
            2
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

    def transform_to_pie_chart(
        self, df: pd.DataFrame, label_column: str, value_column: str
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into pie chart data for part-to-whole relationships.

        Args:
            df: DataFrame containing the data
            label_column: Column name for slice labels (categorical)
            value_column: Column name for slice values (numeric)

        Returns:
            Dict with chart_type='pie_chart' and data points

        Raises:
            TransformationError: If required columns are missing

        Examples:
            >>> df = pd.DataFrame({
            ...     'category': ['Electronics', 'Clothing', 'Food'],
            ...     'sales': [45000, 32000, 18000]
            ... })
            >>> result = transformer.transform_to_pie_chart(df, 'category', 'sales')
            >>> len(result['data'])
            3
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

    def transform_to_heatmap(
        self, df: pd.DataFrame, x_column: str, y_column: str, value_column: str
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into heatmap data for two-dimensional intensity visualization.

        Args:
            df: DataFrame containing the data
            x_column: Column name for x-axis
            y_column: Column name for y-axis
            value_column: Column name for cell values (intensity)

        Returns:
            Dict with chart_type='heatmap', data points, and axis labels

        Raises:
            TransformationError: If required columns are missing

        Examples:
            >>> df = pd.DataFrame({
            ...     'hour': [0, 1, 0, 1],
            ...     'day': ['Mon', 'Mon', 'Tue', 'Tue'],
            ...     'count': [12, 8, 15, 10]
            ... })
            >>> result = transformer.transform_to_heatmap(df, 'hour', 'day', 'count')
            >>> len(result['data'])
            4
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

    def transform_to_funnel_chart(
        self, df: pd.DataFrame, stage_column: str, value_column: str
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into funnel chart data for conversion pipelines.

        Args:
            df: DataFrame containing the data (stages should be in order)
            stage_column: Column name for funnel stages
            value_column: Column name for stage values

        Returns:
            Dict with chart_type='funnel_chart' and data points

        Raises:
            TransformationError: If required columns are missing

        Examples:
            >>> df = pd.DataFrame({
            ...     'stage': ['Visits', 'Sign-ups', 'Purchases'],
            ...     'count': [1000, 300, 100]
            ... })
            >>> result = transformer.transform_to_funnel_chart(df, 'stage', 'count')
            >>> len(result['data'])
            3
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

    def transform_to_stacked_bar_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_columns: List[str],
        category_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into stacked bar chart data for composed comparisons.

        Args:
            df: DataFrame containing the data
            x_column: Column name for x-axis (categories)
            y_columns: List of column names for stacked values
            category_names: Optional custom names for each stack category

        Returns:
            Dict with chart_type='stacked_bar_chart', data points, and metadata

        Raises:
            TransformationError: If required columns are missing

        Examples:
            >>> df = pd.DataFrame({
            ...     'month': ['Jan', 'Feb'],
            ...     'product_a': [100, 150],
            ...     'product_b': [200, 180]
            ... })
            >>> result = transformer.transform_to_stacked_bar_chart(
            ...     df, 'month', ['product_a', 'product_b']
            ... )
            >>> len(result['categories'])
            2
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
            Dict with chart_type='data_table', columns, rows, and pagination metadata

        Examples:
            >>> df = pd.DataFrame({
            ...     'id': [1, 2, 3],
            ...     'name': ['Alice', 'Bob', 'Charlie']
            ... })
            >>> result = transformer.transform_to_data_table(df, page=1, page_size=2)
            >>> len(result['rows'])
            2
            >>> result['total']
            3
        """
        try:
            # Paginate the dataframe
            paginated_df, metadata = paginate_dataframe(df, page, page_size)

            # Build column definitions
            columns = []
            for col in df.columns:
                columns.append({"key": col, "label": format_label(col)})

            # Build row data
            rows = []
            for _, row in paginated_df.iterrows():
                row_data = {}
                for col in df.columns:
                    row_data[col] = safe_get_value(row[col])
                rows.append(row_data)

            return {
                "chart_type": "data_table",
                "columns": columns,
                "rows": rows,
                **metadata,
            }

        except Exception as e:
            raise TransformationError(
                f"Failed to transform data table: {str(e)}",
                chart_type="data_table",
                df_shape=df.shape,
            )

    def transform_to_correlation_heatmap(
        self, df: pd.DataFrame, metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Transform DataFrame into correlation heatmap for statistical analysis.

        Args:
            df: DataFrame containing numeric columns
            metrics: Optional list of column names to correlate (auto-detects if None)

        Returns:
            Dict with chart_type='heatmap', correlation data, and metric names

        Raises:
            TransformationError: If insufficient numeric columns found

        Examples:
            >>> df = pd.DataFrame({
            ...     'revenue': [100, 200, 150],
            ...     'orders': [10, 20, 15],
            ...     'rating': [4.5, 4.8, 4.6]
            ... })
            >>> result = transformer.transform_to_correlation_heatmap(df)
            >>> result['chart_type']
            'heatmap'
        """
        try:
            # Auto-detect numeric columns if metrics not provided
            if metrics is None:
                metrics = get_numeric_columns(df)

            if len(metrics) < 2:
                raise TransformationError(
                    "Need at least 2 numeric columns for correlation",
                    chart_type="correlation_heatmap",
                    df_shape=df.shape,
                )

            validate_columns(df, metrics)

            # Calculate correlation matrix
            corr_matrix = df[metrics].corr()

            # Convert to heatmap format
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
