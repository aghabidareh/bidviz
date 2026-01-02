"""
Custom exceptions for BidViz library.
"""


class BidVizError(Exception):
    """Base exception for all BidViz errors."""

    pass


class TransformationError(BidVizError):
    """
    Exception raised when data transformation fails.

    Attributes:
        message (str): Explanation of the error
        chart_type (str): Type of chart being transformed
        df_shape (tuple): Shape of the DataFrame (rows, columns)
        missing_columns (list): List of missing column names
    """

    def __init__(
        self,
        message: str,
        chart_type: str = None,
        df_shape: tuple = None,
        missing_columns: list = None,
    ):
        self.message = message
        self.chart_type = chart_type
        self.df_shape = df_shape
        self.missing_columns = missing_columns or []
        super().__init__(self.message)

    def __str__(self) -> str:
        details = [self.message]
        if self.chart_type:
            details.append(f"Chart Type: {self.chart_type}")
        if self.df_shape:
            details.append(f"DataFrame Shape: {self.df_shape}")
        if self.missing_columns:
            details.append(f"Missing Columns: {', '.join(self.missing_columns)}")
        return " | ".join(details)


class ValidationError(BidVizError):
    """
    Exception raised when data validation fails.

    Attributes:
        message (str): Explanation of the validation error
        column (str): Column name that failed validation
        validation_type (str): Type of validation that failed
    """

    def __init__(self, message: str, column: str = None, validation_type: str = None):
        self.message = message
        self.column = column
        self.validation_type = validation_type
        super().__init__(self.message)

    def __str__(self) -> str:
        details = [self.message]
        if self.column:
            details.append(f"Column: {self.column}")
        if self.validation_type:
            details.append(f"Validation Type: {self.validation_type}")
        return " | ".join(details)
