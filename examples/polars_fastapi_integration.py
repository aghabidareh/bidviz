"""
FastAPI integration example for BidViz with Polars.

This example shows how to integrate BidViz Polars transformers with a FastAPI backend
to serve chart data to frontend applications. Polars provides significantly better
performance than pandas, especially for larger datasets.
"""

import polars as pl
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from bidviz.exceptions import TransformationError
from bidviz_polars import ChartTransformer

app = FastAPI(
    title="BidViz Polars Demo API",
    description="Example API demonstrating BidViz chart transformations with Polars",
    version="1.0.0",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Polars transformer
transformer = ChartTransformer()


# Mock data functions (replace with actual database queries)
def get_sales_data() -> pl.DataFrame:
    """Get mock sales data."""
    return pl.DataFrame(
        {
            "vendor": [
                "Electronics Inc",
                "Fashion Co",
                "Food Market",
                "Sports Store",
                "Books Plus",
            ],
            "revenue": [125000, 98000, 112000, 87000, 95000],
            "orders": [450, 380, 420, 310, 360],
        }
    )


def get_time_series_data() -> pl.DataFrame:
    """Get mock time series data."""
    import random

    random.seed(42)

    dates = [f"2024-01-{i:02d}" if i <= 30 else f"2024-02-{i-30:02d}" for i in range(1, 31)]
    return pl.DataFrame(
        {
            "date": dates,
            "orders": [random.randint(100, 200) for _ in range(30)],
            "revenue": [random.uniform(5000, 15000) for _ in range(30)],
        }
    )


def get_category_data() -> pl.DataFrame:
    """Get mock category data."""
    return pl.DataFrame(
        {
            "category": ["Electronics", "Clothing", "Food", "Books", "Sports"],
            "sales": [45000, 32000, 28000, 15000, 20000],
        }
    )


def get_dashboard_metrics() -> pl.DataFrame:
    """Get mock dashboard metrics."""
    return pl.DataFrame(
        {
            "total_orders": [1523],
            "total_revenue": [245000.75],
            "avg_order_value": [160.89],
            "customer_satisfaction": [4.7],
        }
    )


def get_order_data(page: int = 1, page_size: int = 50) -> pl.DataFrame:
    """Get mock order data."""
    import random

    random.seed(42)
    total_orders = 500
    return pl.DataFrame(
        {
            "order_id": list(range(1, total_orders + 1)),
            "customer": [f"Customer {i}" for i in range(1, total_orders + 1)],
            "amount": [round(random.uniform(50, 1000), 2) for _ in range(total_orders)],
            "date": [f"2024-01-{(i % 30) + 1:02d}" for i in range(total_orders)],
            "status": [
                random.choice(["Completed", "Pending", "Cancelled"]) for _ in range(total_orders)
            ],
        }
    )


# API Endpoints


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "BidViz Polars Demo API",
        "powered_by": "Polars - High Performance DataFrames",
        "endpoints": [
            "/api/kpi-cards",
            "/api/charts/revenue-by-vendor",
            "/api/charts/sales-trend",
            "/api/charts/category-distribution",
            "/api/charts/orders-table",
        ],
    }


@app.get("/api/kpi-cards")
async def get_kpi_cards():
    """Get KPI cards for dashboard."""
    try:
        df = get_dashboard_metrics()
        result = transformer.transform_to_kpi_cards(df)
        return result
    except TransformationError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/charts/revenue-by-vendor")
async def get_revenue_by_vendor(chart_type: str = Query("bar", enum=["bar", "pie"])):
    """
    Get revenue by vendor chart.

    Args:
        chart_type: Type of chart (bar or pie)
    """
    try:
        df = get_sales_data()

        if chart_type == "bar":
            result = transformer.transform_to_bar_chart(df, x_column="vendor", y_column="revenue")
        elif chart_type == "pie":
            result = transformer.transform_to_pie_chart(
                df, label_column="vendor", value_column="revenue"
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid chart type")

        return result
    except TransformationError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/charts/sales-trend")
async def get_sales_trend(metric: str = Query("orders", enum=["orders", "revenue"])):
    """
    Get sales trend over time.

    Args:
        metric: Metric to display (orders or revenue)
    """
    try:
        df = get_time_series_data()
        result = transformer.transform_to_line_chart(
            df, x_column="date", y_column=metric, series_name=f"Daily {metric.title()}"
        )
        return result
    except TransformationError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/charts/multi-metric-trend")
async def get_multi_metric_trend():
    """Get multiple metrics trend comparison."""
    try:
        df = get_time_series_data()

        # Polars normalization - showcase Polars expressions
        df = df.with_columns(
            [
                ((pl.col("orders") - pl.col("orders").min()) / (pl.col("orders").max() - pl.col("orders").min()) * 100).alias("orders_normalized"),
                ((pl.col("revenue") - pl.col("revenue").min()) / (pl.col("revenue").max() - pl.col("revenue").min()) * 100).alias("revenue_normalized"),
            ]
        )

        result = transformer.transform_to_multi_line_chart(
            df,
            x_column="date",
            y_columns=["orders_normalized", "revenue_normalized"],
            series_names=["Orders (Normalized)", "Revenue (Normalized)"],
        )
        return result
    except TransformationError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/charts/category-distribution")
async def get_category_distribution():
    """Get category sales distribution."""
    try:
        df = get_category_data()
        result = transformer.transform_to_pie_chart(df, label_column="category", value_column="sales")
        return result
    except TransformationError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/charts/orders-table")
async def get_orders_table(page: int = Query(1, ge=1), page_size: int = Query(50, ge=10, le=100)):
    """
    Get paginated orders table.

    Args:
        page: Page number (starting from 1)
        page_size: Number of records per page (10-100)
    """
    try:
        df = get_order_data()
        result = transformer.transform_to_data_table(df, page=page, page_size=page_size)
        return result
    except TransformationError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/charts/vendor-comparison")
async def get_vendor_comparison():
    """Get stacked comparison of vendors across metrics."""
    try:
        df = get_sales_data()
        result = transformer.transform_to_stacked_bar_chart(
            df,
            x_column="vendor",
            y_columns=["revenue", "orders"],
            category_names=["Revenue ($)", "Orders (count)"],
        )
        return result
    except TransformationError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/charts/correlation")
async def get_correlation_analysis():
    """Get correlation analysis between metrics."""
    try:
        df = get_time_series_data()

        # Polars expressions for calculated columns
        df = df.with_columns(
            [
                (pl.col("revenue") / pl.col("orders")).alias("avg_order_value"),
                (pl.col("revenue").pct_change().fill_null(0) * 100).alias("growth_rate"),
            ]
        )

        result = transformer.transform_to_correlation_heatmap(df)
        return result
    except TransformationError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/performance-info")
async def get_performance_info():
    """Get information about Polars performance benefits."""
    return {
        "library": "Polars",
        "advantages": [
            "Lazy evaluation with query optimization",
            "Parallel execution on all CPU cores",
            "Memory-efficient columnar storage",
            "Zero-copy operations where possible",
            "2-10x faster than pandas for typical operations",
            "Better scaling for datasets > 100K rows",
        ],
        "use_cases": [
            "Real-time analytics dashboards",
            "Large dataset transformations",
            "High-throughput API endpoints",
            "ETL pipelines",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    print("Starting BidViz Polars Demo API...")
    print("Performance benefits: Polars provides significantly better performance than pandas")
    print("API docs available at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
