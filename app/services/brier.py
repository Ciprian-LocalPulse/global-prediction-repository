"""
Brier score calculation.

The Brier score is just mean squared error applied to a probability
forecast against a binary outcome. Given a forecast probability p (as a
fraction between 0 and 1) and an outcome o in {0, 1}:

    BS = (p - o)^2

For a single forecast this collapses to one term; the "mean" in "mean
squared error" matters when you're scoring a forecaster across many
predictions, which is what app.services.reputation does.

A perfectly confident and correct forecast (p=1, o=1) scores 0. A
perfectly confident and wrong forecast (p=1, o=0) scores 1 — the worst
possible outcome. A forecaster who always says 50% scores 0.25 regardless
of what happens, which is exactly why 0.25 is the benchmark "no better
than a coin flip" line worth comparing everyone else against.
"""


def calculate_brier_score(probability_estimate: float, outcome: bool) -> float:
    """
    Args:
        probability_estimate: forecast probability as a percentage (0-100),
            matching how it's stored on Prediction/Forecast rows.
        outcome: True if the prediction resolved True, False otherwise.

    Returns:
        Brier score in [0, 1], where lower is better.
    """
    if not 0 <= probability_estimate <= 100:
        raise ValueError("probability_estimate must be between 0 and 100")

    p = probability_estimate / 100.0
    o = 1.0 if outcome else 0.0
    return round((p - o) ** 2, 6)


def mean_brier_score(scores: list[float]) -> float | None:
    """Average Brier score across a set of resolved forecasts.

    Returns None for an empty list rather than raising, since "this user
    has no resolved forecasts yet" is a normal state, not an error.
    """
    if not scores:
        return None
    return round(sum(scores) / len(scores), 6)
