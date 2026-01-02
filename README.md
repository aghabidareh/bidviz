# BidViz

[![PyPI version](https://badge.fury.io/py/bidviz.svg)](https://badge.fury.io/py/bidviz)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/aghabidareh/bidviz/workflows/Tests/badge.svg)](https://github.com/aghabidareh/bidviz/actions)
[![Coverage](https://codecov.io/gh/aghabidareh/bidviz/branch/main/graph/badge.svg)](https://codecov.io/gh/aghabidareh/bidviz)

A powerful, configurable backend visualization data transformation library designed to bridge the gap between raw data and frontend charting libraries. Built with pandas at its core, BidViz provides a comprehensive suite of tools for data cleaning, transformation, and formatting optimized for analytics dashboards and data visualization applications.

## Features

- **12+ Chart Type Transformations**: Support for KPI cards, bar charts, line charts, pie charts, heatmaps, funnels, tables, and more
- **Automatic Data Cleaning**: NaN handling, type conversion, and null sanitization
- **Human-Readable Formatting**: Intelligent label generation from column names
- **Built-in Pagination**: Server-side pagination for data tables
- **Frontend-Ready Output**: JSON-serializable structures optimized for charting libraries
- **Statistical Analysis**: Correlation matrices with heatmap data generation
- **Highly Configurable**: Custom column mappings, formatting rules, and transformation behaviors
- **Framework Agnostic**: Works with any frontend (React, Vue, Angular) and any charting library (Chart.js, D3, Plotly, Recharts)

## Installation

```bash
pip install bidviz
```

For development:

```bash
pip install bidviz[dev]
```

## Quick Start

```python
import pandas as pd
from bidviz import ChartTransformer

# Initialize the transformer
transformer = ChartTransformer()

# Sample data
df = pd.DataFrame({
    'vendor': ['Vendor A', 'Vendor B', 'Vendor C'],
    'revenue': [125000, 98000, 112000]
})

# Transform to bar chart
result = transformer.transform_to_bar_chart(
    df=df,
    x_column='vendor',
    y_column='revenue'
)

print(result)
# {
#     "chart_type": "bar_chart",
#     "data": [
#         {"x": "Vendor A", "y": 125000, "label": "Vendor A"},
#         {"x": "Vendor B", "y": 98000, "label": "Vendor B"},
#         {"x": "Vendor C", "y": 112000, "label": "Vendor C"}
#     ],
#     "x_label": "Vendor",
#     "y_label": "Revenue"
# }
```

## Supported Chart Types

| Chart Type | Method | Use Case |
|------------|--------|----------|
| **KPI Cards** | `transform_to_kpi_cards()` | Dashboard metrics, summary numbers |
| **Bar Chart** | `transform_to_bar_chart()` | Categorical comparisons, rankings |
| **Line Chart** | `transform_to_line_chart()` | Time series, trends |
| **Multi-Line Chart** | `transform_to_multi_line_chart()` | Multiple time series comparisons |
| **Pie Chart** | `transform_to_pie_chart()` | Part-to-whole relationships |
| **Heatmap** | `transform_to_heatmap()` | Two-dimensional relationships |
| **Funnel Chart** | `transform_to_funnel_chart()` | Conversion pipelines |
| **Stacked Bar Chart** | `transform_to_stacked_bar_chart()` | Composed categorical comparisons |
| **Data Table** | `transform_to_data_table()` | Tabular data with pagination |
| **Correlation Heatmap** | `transform_to_correlation_heatmap()` | Statistical relationships |

## Usage Examples

### KPI Cards

```python
# Single-row DataFrame with metrics
df = pd.DataFrame({
    'total_orders': [150],
    'revenue': [45000.50],
    'satisfaction_rate': [94.2]
})

result = transformer.transform_to_kpi_cards(df)
# Returns list of KPI cards with labels, values, and keys
```

### Line Chart with Time Series

```python
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30),
    'orders': [152, 168, 145, ...]  # 30 values
})

result = transformer.transform_to_line_chart(
    df=df,
    x_column='date',
    y_column='orders',
    series_name='Daily Orders'
)
```

### Multi-Line Chart

```python
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=30),
    'vendor_a': [...],
    'vendor_b': [...],
    'vendor_c': [...]
})

result = transformer.transform_to_multi_line_chart(
    df=df,
    x_column='date',
    y_columns=['vendor_a', 'vendor_b', 'vendor_c'],
    series_names=['Vendor A', 'Vendor B', 'Vendor C']
)
```

### Data Table with Pagination

```python
df = pd.DataFrame({
    'order_id': range(1, 1001),
    'customer': [f'Customer {i}' for i in range(1, 1001)],
    'amount': [...]  # 1000 values
})

result = transformer.transform_to_data_table(
    df=df,
    page=1,
    page_size=50
)
# Returns paginated data with metadata
```

### Correlation Heatmap

```python
df = pd.DataFrame({
    'revenue': [...],
    'orders': [...],
    'rating': [...],
    'shipping_days': [...]
})

result = transformer.transform_to_correlation_heatmap(df)
# Auto-detects numeric columns and generates correlation matrix
```

## Integration with Web Frameworks

### FastAPI

```python
from fastapi import FastAPI, Query
from bidviz import ChartTransformer
import pandas as pd

app = FastAPI()
transformer = ChartTransformer()

@app.get("/api/charts/revenue")
async def get_revenue_chart(chart_type: str = Query("bar")):
    # Fetch data from database
    df = get_revenue_data()

    if chart_type == "bar":
        return transformer.transform_to_bar_chart(
            df, x_column='vendor', y_column='revenue'
        )
    elif chart_type == "line":
        return transformer.transform_to_line_chart(
            df, x_column='date', y_column='revenue'
        )
```

### Flask

```python
from flask import Flask, jsonify
from bidviz import ChartTransformer

app = Flask(__name__)
transformer = ChartTransformer()

@app.route('/api/charts/sales')
def sales_chart():
    df = get_sales_data()
    result = transformer.transform_to_pie_chart(
        df, label_column='category', value_column='sales'
    )
    return jsonify(result)
```

## Frontend Integration

### React with Recharts

```javascript
import { BarChart, Bar, XAxis, YAxis } from 'recharts';

function RevenueChart() {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    fetch('/api/charts/revenue?chart_type=bar')
      .then(res => res.json())
      .then(data => setChartData(data));
  }, []);

  if (!chartData) return <div>Loading...</div>;

  return (
    <BarChart data={chartData.data}>
      <XAxis dataKey="x" label={chartData.x_label} />
      <YAxis label={chartData.y_label} />
      <Bar dataKey="y" fill="#8884d8" />
    </BarChart>
  );
}
```

### Chart.js

```javascript
const response = await fetch('/api/charts/revenue?chart_type=line');
const chartData = await response.json();

new Chart(ctx, {
  type: 'line',
  data: {
    labels: chartData.data.map(d => d.x),
    datasets: [{
      label: chartData.series_name,
      data: chartData.data.map(d => d.y)
    }]
  }
});
```

## Data Handling

### NaN Handling

All transformations automatically handle pandas NaN values:
- **Numeric NaN** → `null` in JSON
- **String/Empty NaN** → `null` in JSON
- All computations work safely with NaN values

### Type Conversion

| Input Type | Output Type | Notes |
|------------|-------------|-------|
| `int64` | `float` | Safe for JSON serialization |
| `float64` | `float` | Precision preserved |
| `datetime64` | `string` | ISO format |
| `object` | `string` | String representation |
| `boolean` | `boolean` | Preserved |

### Label Formatting

Automatic snake_case to Title Case conversion:
- `total_gmv` → `"Total Gmv"`
- `customer_id` → `"Customer Id"`
- `avg_days_to_ship` → `"Avg Days To Ship"`

## Error Handling

```python
from bidviz.exceptions import TransformationError

try:
    result = transformer.transform_to_bar_chart(df, 'category', 'value')
except TransformationError as e:
    print(f"Error: {e.message}")
    print(f"Chart Type: {e.chart_type}")
    print(f"DataFrame Shape: {e.df_shape}")
    print(f"Missing Columns: {e.missing_columns}")
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/aghabidareh/bidviz.git
cd bidviz

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_transformer.py

# Run with verbose output
pytest -v

# Generate HTML coverage report
pytest --cov=bidviz --cov-report=html
```

### Code Quality

```bash
# Format code with black
black bidviz tests

# Sort imports
isort bidviz tests

# Check code style
flake8 bidviz tests

# Type checking
mypy bidviz
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the existing code style.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes.

## Roadmap

- [ ] Advanced value formatting pipeline
- [ ] Data validation framework
- [ ] Aggregation pipeline
- [ ] Multi-chart dashboard builder
- [ ] Real-time streaming support
- [ ] Export & report generation (PDF, Excel)
- [ ] Caching layer
- [ ] Plugin system
- [ ] Multi-language support
- [ ] Performance profiling tools

## Acknowledgments

- Built with [pandas](https://pandas.pydata.org/)
- Inspired by the need for seamless backend-to-frontend data transformation
- Thanks to all contributors and users of this library

## Contact

Mohammad Amin Khara - kharama8709@gmail.com

Project Link: [https://github.com/aghabidareh/bidviz](https://github.com/aghabidareh/bidviz)