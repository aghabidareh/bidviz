# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-29

### Added
- **Polars Support**: Complete high-performance Polars DataFrame support
  - New `bidviz_polars` module with all transformer implementations
  - 2-10x faster transformations on large datasets (100K+ rows)
  - Parallel processing and lazy evaluation support
  - Memory-efficient columnar operations
  - Zero-copy operations where possible
- Polars-specific utility functions in `bidviz_polars/utils.py`
- Comprehensive test suite for Polars transformers (90+ tests)
- Polars usage examples:
  - `examples/polars_basic_usage.py` - All chart type examples
  - `examples/polars_fastapi_integration.py` - API integration example
- Performance comparison documentation
- Updated README with Polars Quick Start and performance benchmarks

### Technical Details
- Added `polars>=0.20.0` as core dependency
- Modular architecture mirrors pandas implementation
- All 10+ chart types supported with Polars
- Same JSON output format as pandas version
- Full API compatibility with pandas transformers

### Performance
- 2x faster on 1K row datasets
- 6x faster on 10K row datasets
- 7x faster on 100K row datasets
- 10x faster on 1M+ row datasets

## [1.0.0] - 2025-01-02

### Added
- Initial release of BidViz
- ChartTransformer service with 10+ chart type transformations
- KPI Cards transformation
- Bar Chart transformation
- Line Chart transformation
- Multi-Line Chart transformation
- Pie Chart transformation
- Heatmap transformation
- Funnel Chart transformation
- Stacked Bar Chart transformation
- Data Table transformation with pagination
- Correlation Heatmap transformation
- Automatic NaN handling and type conversion
- Human-readable label formatting
- Comprehensive test suite with 95%+ coverage
- Complete API documentation with docstrings
- Exception handling with custom error types
- Utility functions for data cleaning and formatting
- Support for Python 3.9+
- CI/CD pipeline with GitHub Actions
- PyPI publishing workflow
- MIT License

### Documentation
- Complete README with usage examples
- API reference documentation
- Integration examples for FastAPI and Flask
- Frontend integration examples for React and Chart.js
- Development setup guide
- Contributing guidelines

### Testing
- 100+ unit tests
- Test fixtures for common data scenarios
- Coverage reporting
- Multi-platform testing (Ubuntu, Windows, macOS)
- Multi-version Python testing (3.9, 3.10, 3.11, 3.12)

### CI/CD
- Automated testing on push and pull requests
- Code quality checks (black, isort, flake8, mypy)
- Coverage reporting to Codecov
- Automated PyPI publishing on release
- Documentation building and validation

[1.0.0]: https://github.com/aghabidareh/bidviz/releases/tag/v1.0.0