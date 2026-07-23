"""
The Reputation Engine.

Converts a user's history of resolved Brier scores into the single
global_accuracy_score stored on their User row (0-100, higher is better).
That score is what app.services.crowd_wisdom uses to weight forecasts in
the consensus calculation, and what the leaderboard sorts on.

The conversion is deliberately simple:

    accuracy_score = (1 - mean_brier_score) * 100

A user who is always exactly right (mean Brier = 0) scores 100. A user who
is always maximally wrong (mean Brier = 1) scores 0. A user who forecasts
like a coin flip every time (mean Brier = 0.25) scores 75 — reflecting
that being appropriately uncertain about genuinely uncertain questions is
not the same as being a bad forecaster.

New users start at 50 (see the User model default) rather than 0, so a
single early bad forecast doesn't sink them before they have enough
history for the score to mean anything.
"""

from sqlalchemy.orm import Session

from app.models.forecast import Forecast
from app.models.user import User
from app.services.brier import mean_brier_score


def recalculate_user_reputation(db: Session, user: User) -> User:
    resolved_scores = [
        f.brier_score
        for f in user.forecasts
        if f.brier_score is not None
    ]

    avg = mean_brier_score(resolved_scores)
    if avg is not None:
        user.global_accuracy_score = round((1 - avg) * 100, 2)
        user.resolved_forecast_count = len(resolved_scores)
        db.add(user)

    return user


def recalculate_all_reputations_for_prediction(db: Session, prediction_id: str) -> None:
    """Called after a prediction resolves, to update every forecaster who
    had a stake in it. Kept separate from the resolution service itself
    so it can be unit tested without going through the full resolution
    flow.
    """
    forecasts = (
        db.query(Forecast)
        .filter(Forecast.prediction_id == prediction_id)
        .all()
    )
    for forecast in forecasts:
        recalculate_user_reputation(db, forecast.user)
    db.commit()
