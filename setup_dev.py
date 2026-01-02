"""Setup script for installing BidViz in development mode."""
import subprocess
import sys


def main():
    """Install BidViz in development mode with all dependencies."""
    print("Installing BidViz in development mode...")
    print("=" * 50)

    # Upgrade pip
    print("\n1. Upgrading pip...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    # Install package in editable mode with dev dependencies
    print("\n2. Installing BidViz with development dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", ".[dev]"])

    print("\n" + "=" * 50)
    print("Installation complete!")
    print("\nYou can now:")
    print("  - Run tests: pytest")
    print("  - Check coverage: pytest --cov=bidviz --cov-report=html")
    print("  - Format code: black bidviz tests")
    print("  - Sort imports: isort bidviz tests")
    print("  - Lint code: flake8 bidviz tests")
    print("  - Run examples: python examples/basic_usage.py")


if __name__ == "__main__":
    main()