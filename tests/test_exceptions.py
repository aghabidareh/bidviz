"""Tests for exception classes."""

import pytest

from bidviz.exceptions import BidVizError, TransformationError, ValidationError


class TestBidVizError:
    """Tests for base BidVizError exception."""

    def test_base_exception_creation(self):
        """Test creating base exception."""
        error = BidVizError("Test error")
        assert str(error) == "Test error"

    def test_base_exception_inheritance(self):
        """Test that BidVizError inherits from Exception."""
        assert issubclass(BidVizError, Exception)


class TestTransformationError:
    """Tests for TransformationError exception."""

    def test_basic_transformation_error(self):
        """Test creating basic TransformationError."""
        error = TransformationError("Transformation failed")
        assert error.message == "Transformation failed"
        assert error.chart_type is None
        assert error.df_shape is None
        assert error.missing_columns == []

    def test_transformation_error_with_all_attributes(self):
        """Test TransformationError with all attributes."""
        error = TransformationError(
            message="Column not found",
            chart_type="bar_chart",
            df_shape=(100, 5),
            missing_columns=["col1", "col2"],
        )

        assert error.message == "Column not found"
        assert error.chart_type == "bar_chart"
        assert error.df_shape == (100, 5)
        assert error.missing_columns == ["col1", "col2"]

    def test_transformation_error_string_representation(self):
        """Test string representation of TransformationError."""
        error = TransformationError(
            message="Failed to transform",
            chart_type="line_chart",
            df_shape=(50, 3),
            missing_columns=["date"],
        )

        error_str = str(error)
        assert "Failed to transform" in error_str
        assert "line_chart" in error_str
        assert "(50, 3)" in error_str
        assert "date" in error_str

    def test_transformation_error_minimal_string(self):
        """Test string representation with minimal attributes."""
        error = TransformationError("Simple error")
        assert str(error) == "Simple error"

    def test_transformation_error_inheritance(self):
        """Test TransformationError inheritance."""
        assert issubclass(TransformationError, BidVizError)
        assert issubclass(TransformationError, Exception)


class TestValidationError:
    """Tests for ValidationError exception."""

    def test_basic_validation_error(self):
        """Test creating basic ValidationError."""
        error = ValidationError("Validation failed")
        assert error.message == "Validation failed"
        assert error.column is None
        assert error.validation_type is None

    def test_validation_error_with_all_attributes(self):
        """Test ValidationError with all attributes."""
        error = ValidationError(
            message="Invalid value", column="revenue", validation_type="numeric"
        )

        assert error.message == "Invalid value"
        assert error.column == "revenue"
        assert error.validation_type == "numeric"

    def test_validation_error_string_representation(self):
        """Test string representation of ValidationError."""
        error = ValidationError(message="Value out of range", column="age", validation_type="range")

        error_str = str(error)
        assert "Value out of range" in error_str
        assert "age" in error_str
        assert "range" in error_str

    def test_validation_error_minimal_string(self):
        """Test string representation with minimal attributes."""
        error = ValidationError("Simple validation error")
        assert str(error) == "Simple validation error"

    def test_validation_error_inheritance(self):
        """Test ValidationError inheritance."""
        assert issubclass(ValidationError, BidVizError)
        assert issubclass(ValidationError, Exception)


class TestExceptionRaising:
    """Tests for raising and catching exceptions."""

    def test_catching_transformation_error(self):
        """Test catching TransformationError."""
        with pytest.raises(TransformationError) as exc_info:
            raise TransformationError("Test", chart_type="bar")

        assert exc_info.value.chart_type == "bar"

    def test_catching_validation_error(self):
        """Test catching ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            raise ValidationError("Test", column="col1")

        assert exc_info.value.column == "col1"

    def test_catching_as_base_exception(self):
        """Test catching BidViz errors as base exception."""
        with pytest.raises(BidVizError):
            raise TransformationError("Test error")

        with pytest.raises(BidVizError):
            raise ValidationError("Test error")
