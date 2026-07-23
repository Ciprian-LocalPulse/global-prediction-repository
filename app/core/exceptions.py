class GPRException(Exception):
    """Base class for application-specific errors."""


class PredictionNotOpenError(GPRException):
    """Raised when a forecast is submitted against a prediction that isn't open."""


class InvalidResolutionError(GPRException):
    """Raised when a prediction is resolved in a state that doesn't allow it."""


class DuplicateForecastError(GPRException):
    """Raised when a user tries to forecast the same prediction twice.

    We update in place instead of silently creating a second row — see
    app/routers/forecasts.py.
    """
