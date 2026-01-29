"""
Example usage of BidViz library with Polars demonstrating various chart transformations.

This example shows how to use BidViz with Polars DataFrames for high-performance
data transformations. Polars provides significant performance benefits over pandas,
especially for larger datasets.
"""

import polars as pl

from bidviz_polars import ChartTransformer


def main():
    """Run example transformations with Polars."""
    # Initialize Polars transformer
    transformer = ChartTransformer()

    print("BidViz Polars Examples\n" + "=" * 50 + "\n")

    # Example 1: KPI Cards
    print("1. KPI Cards")
    print("-" * 50)
    kpi_df = pl.DataFrame(
        {
            "total_orders": [1523],
            "total_revenue": [245000.75],
            "avg_order_value": [160.89],
            "customer_satisfaction": [4.7],
        }
    )
    kpi_result = transformer.transform_to_kpi_cards(kpi_df)
    print(f"Chart Type: {kpi_result['chart_type']}")
    print(f"Number of KPIs: {len(kpi_result['data'])}")
    print(f"First KPI: {kpi_result['data'][0]}")
    print()

    # Example 2: Bar Chart
    print("2. Bar Chart")
    print("-" * 50)
    bar_df = pl.DataFrame(
        {
            "vendor": ["Electronics Inc", "Fashion Co", "Food Market", "Sports Store"],
            "revenue": [125000, 98000, 112000, 87000],
        }
    )
    bar_result = transformer.transform_to_bar_chart(bar_df, "vendor", "revenue")
    print(f"Chart Type: {bar_result['chart_type']}")
    print(f"X Label: {bar_result['x_label']}")
    print(f"Y Label: {bar_result['y_label']}")
    print(f"Data Points: {len(bar_result['data'])}")
    print()

    # Example 3: Line Chart
    print("3. Line Chart")
    print("-" * 50)
    line_df = pl.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-01-06", "2024-01-07"],
            "daily_orders": [152, 168, 145, 175, 160, 155, 170],
        }
    )
    line_result = transformer.transform_to_line_chart(
        line_df, "date", "daily_orders", series_name="Daily Orders"
    )
    print(f"Chart Type: {line_result['chart_type']}")
    print(f"Series Name: {line_result['series_name']}")
    print(f"First Data Point: {line_result['data'][0]}")
    print()

    # Example 4: Multi-Line Chart
    print("4. Multi-Line Chart")
    print("-" * 50)
    multi_line_df = pl.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"],
            "product_a_sales": [100, 120, 115, 130, 125],
            "product_b_sales": [80, 85, 90, 95, 100],
            "product_c_sales": [60, 65, 70, 75, 80],
        }
    )
    multi_result = transformer.transform_to_multi_line_chart(
        multi_line_df,
        "date",
        ["product_a_sales", "product_b_sales", "product_c_sales"],
        series_names=["Product A", "Product B", "Product C"],
    )
    print(f"Chart Type: {multi_result['chart_type']}")
    print(f"Number of Series: {len(multi_result['series'])}")
    print(f"First Series: {multi_result['series'][0]['name']}")
    print()

    # Example 5: Pie Chart
    print("5. Pie Chart")
    print("-" * 50)
    pie_df = pl.DataFrame(
        {
            "category": ["Electronics", "Clothing", "Food", "Books", "Other"],
            "sales": [45000, 32000, 28000, 15000, 10000],
        }
    )
    pie_result = transformer.transform_to_pie_chart(pie_df, "category", "sales")
    print(f"Chart Type: {pie_result['chart_type']}")
    print(f"Number of Slices: {len(pie_result['data'])}")
    print(f"Largest Category: {pie_result['data'][0]}")
    print()

    # Example 6: Heatmap
    print("6. Heatmap")
    print("-" * 50)
    heatmap_df = pl.DataFrame(
        {
            "hour": [0, 1, 2, 0, 1, 2] * 2,
            "day": ["Monday"] * 3 + ["Tuesday"] * 3 + ["Wednesday"] * 3 + ["Thursday"] * 3,
            "order_count": [12, 8, 15, 10, 14, 11, 18, 9, 13, 16, 11, 14],
        }
    )
    heatmap_result = transformer.transform_to_heatmap(heatmap_df, "hour", "day", "order_count")
    print(f"Chart Type: {heatmap_result['chart_type']}")
    print(f"Data Points: {len(heatmap_result['data'])}")
    print(f"Value Label: {heatmap_result['value_label']}")
    print()

    # Example 7: Funnel Chart
    print("7. Funnel Chart")
    print("-" * 50)
    funnel_df = pl.DataFrame(
        {
            "stage": ["Website Visits", "Product Views", "Add to Cart", "Checkout", "Purchase"],
            "count": [10000, 5000, 2000, 1000, 500],
        }
    )
    funnel_result = transformer.transform_to_funnel_chart(funnel_df, "stage", "count")
    print(f"Chart Type: {funnel_result['chart_type']}")
    print(f"Stages: {len(funnel_result['data'])}")
    conversion_rate = (
        funnel_result["data"][-1]["value"] / funnel_result["data"][0]["value"] * 100
    )
    print(f"Conversion Rate: {conversion_rate:.2f}%")
    print()

    # Example 8: Stacked Bar Chart
    print("8. Stacked Bar Chart")
    print("-" * 50)
    stacked_df = pl.DataFrame(
        {
            "month": ["January", "February", "March", "April"],
            "online_sales": [50000, 55000, 52000, 58000],
            "store_sales": [30000, 32000, 31000, 35000],
            "wholesale_sales": [20000, 21000, 22000, 23000],
        }
    )
    stacked_result = transformer.transform_to_stacked_bar_chart(
        stacked_df,
        "month",
        ["online_sales", "store_sales", "wholesale_sales"],
        category_names=["Online", "Store", "Wholesale"],
    )
    print(f"Chart Type: {stacked_result['chart_type']}")
    print(f"Categories: {stacked_result['categories']}")
    print(f"Months: {len(stacked_result['data'])}")
    print()

    # Example 9: Data Table with Pagination
    print("9. Data Table")
    print("-" * 50)
    table_df = pl.DataFrame(
        {
            "order_id": list(range(1, 151)),
            "customer_name": [f"Customer {i}" for i in range(1, 151)],
            "order_amount": [50.0 + (i * 6.5) for i in range(150)],
            "status": (["Completed", "Pending", "Cancelled"] * 50)[:150],
        }
    )
    table_result = transformer.transform_to_data_table(table_df, page=1, page_size=20)
    print(f"Chart Type: {table_result['chart_type']}")
    print(f"Total Records: {table_result['total']}")
    print(f"Page: {table_result['page']}/{table_result['total_pages']}")
    print(f"Rows on Page: {len(table_result['rows'])}")
    print(f"Columns: {[col['label'] for col in table_result['columns']]}")
    print()

    # Example 10: Correlation Heatmap
    print("10. Correlation Heatmap")
    print("-" * 50)
    # Create sample data with some correlation
    import random

    random.seed(42)
    orders = [random.randint(10, 100) for _ in range(100)]
    revenue = [order * 50 + random.gauss(0, 500) for order in orders]

    corr_df = pl.DataFrame(
        {
            "revenue": revenue,
            "orders": orders,
            "customer_rating": [random.uniform(3.5, 5.0) for _ in range(100)],
            "shipping_days": [random.randint(1, 10) for _ in range(100)],
        }
    )

    corr_result = transformer.transform_to_correlation_heatmap(corr_df)
    print(f"Chart Type: {corr_result['chart_type']}")
    print(f"Metrics: {corr_result['metrics']}")
    print(f"Correlation Matrix Size: {len(corr_result['data'])} points")
    print(f"Value Label: {corr_result['value_label']}")
    print()

    # Example 11: Handling Null Values
    print("11. Handling Null Values")
    print("-" * 50)
    null_df = pl.DataFrame(
        {
            "product": ["Product A", "Product B", None, "Product D"],
            "sales": [1000, None, 1500, 2000],
        }
    )
    null_result = transformer.transform_to_bar_chart(null_df, "product", "sales")
    print(f"Data with Null: {null_result['data']}")
    print(f"Note: Null values are converted to None (null in JSON)")
    print()

    # Example 12: Performance Benefits with Polars
    print("12. Performance Benefits with Polars")
    print("-" * 50)
    print("Polars advantages:")
    print("- Lazy evaluation for query optimization")
    print("- Parallel execution on all CPU cores")
    print("- Memory-efficient columnar storage")
    print("- Zero-copy operations where possible")
    print("- Significantly faster for large datasets (100K+ rows)")
    print()

    print("=" * 50)
    print("Examples completed successfully!")


if __name__ == "__main__":
    main()
