# Contributing to BidViz

Thank you for considering contributing to BidViz! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, BidViz version)
- **Code sample** demonstrating the issue

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear title and description**
- **Use case** explaining why this would be useful
- **Examples** of how it would work
- **Possible implementation** (if you have ideas)

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Install development dependencies**: `pip install -e ".[dev]"`
3. **Make your changes**
4. **Add tests** for your changes
5. **Ensure tests pass**: `pytest`
6. **Check code quality**:
   - Format: `black bidviz tests`
   - Sort imports: `isort bidviz tests`
   - Lint: `flake8 bidviz tests`
   - Type check: `mypy bidviz`
7. **Update documentation** as needed
8. **Commit your changes** with a clear commit message
9. **Push to your fork** and submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/bidviz.git
cd bidviz

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=bidviz --cov-report=html

# Run specific test file
pytest tests/test_transformer.py

# Run specific test
pytest tests/test_transformer.py::TestBarChart::test_basic_bar_chart
```

## Code Style

- **Python version**: 3.9+
- **Line length**: 100 characters
- **Formatter**: Black
- **Import sorting**: isort
- **Linter**: flake8
- **Type hints**: Use type hints for all public APIs
- **Docstrings**: Google-style docstrings for all public functions/classes

### Example Function

```python
def transform_data(
    df: pd.DataFrame,
    column: str,
    format_type: str = "default"
) -> Dict[str, Any]:
    """
    Transform DataFrame data to specified format.

    Args:
        df: Input DataFrame
        column: Column name to transform
        format_type: Type of formatting to apply

    Returns:
        Dictionary containing transformed data

    Raises:
        ValueError: If column doesn't exist in DataFrame

    Examples:
        >>> df = pd.DataFrame({'col': [1, 2, 3]})
        >>> transform_data(df, 'col')
        {'data': [1, 2, 3]}
    """
    pass
```

## Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be 50 characters or less
- Reference issues and pull requests when applicable

Examples:
```
Add correlation heatmap transformation
Fix NaN handling in bar chart transformer
Update documentation for line chart API
Refactor pagination utility function
```

## Adding New Chart Types

When adding a new chart type:

1. Add the transformation method to `ChartTransformer` class
2. Include comprehensive docstring with examples
3. Add tests in `tests/test_transformer.py`
4. Add test fixtures in `tests/conftest.py` if needed
5. Update `README.md` with the new chart type
6. Add usage example in the documentation

## Documentation

- Update docstrings when changing function signatures
- Add examples to docstrings
- Update README.md for user-facing changes
- Update CHANGELOG.md following Keep a Changelog format

## Release Process

Releases are handled by maintainers:

1. Update version in `pyproject.toml` and `bidviz/__init__.py`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag -a v1.x.x -m "Release v1.x.x"`
4. Push tag: `git push origin v1.x.x`
5. Create GitHub release (triggers PyPI publishing)

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.