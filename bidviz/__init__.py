"""
BidViz - Backend Visualization Data Transformation Library

A powerful, configurable backend visualization data transformation library designed to bridge
the gap between raw data and frontend charting libraries.
"""

__version__ = "1.0.0"
__author__ = "Mohammad Amin Khara"

from bidviz.exceptions import TransformationError, ValidationError
from bidviz.transformer import ChartTransformer

__all__ = ["ChartTransformer", "TransformationError", "ValidationError"]
