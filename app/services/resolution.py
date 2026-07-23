"""
Resolving a prediction: the moment a hypothesis stops being a guess and
becomes a graded one.

This is the one place in the codebase where all three pieces come
together — Brier scoring, per-forecast scoring, and the reputation
engine — so it's worth walking through what happens, in order, when an
Oracle resolves a prediction:

1. The prediction's status moves to Resolved_True, Resolved_False, or
   Ambiguous.
2. If it resolved to True/False, every Forecast row attached to it
   (including the creator's own initial probability_estimate, which is
   scored the same way) gets a Brier score.
3. Every user who forecasted on this prediction has their
   global_accuracy_score recalculated from their updated history.

Ambiguous resolutions skip steps 2 and 3 entirely — a question whose
resolution criteria turned out to be unanswerable shouldn't count for or
against anyone's track record.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.enums import PredictionStatus
from app.core.exceptions import InvalidResolutionError
from app.models.forecast import Forecast
from app.models.prediction import Prediction
from app.services.brier import calculate_brier_score
from app.services.reputation import recalculate_all_reputations_for_prediction


def resolve_prediction(db: Session, prediction: Prediction, outcome: bool | None, ambiguous: bool = False) -> Prediction:
    if prediction.status not in (PredictionStatus.OPEN, PredictionStatus.CLOSED):
        raise InvalidResolutionError(
            f"Prediction {prediction.id} is already {prediction.status.value} and cannot be re-resolved"
        )

    if ambiguous:
        prediction.status = PredictionStatus.AMBIGUOUS
        prediction.resolved_at = datetime.now(timezone.utc)
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction

    if outcome is None:
        raise InvalidResolutionError("outcome must be provided unless the resolution is ambiguous")

    prediction.status = PredictionStatus.RESOLVED_TRUE if outcome else PredictionStatus.RESOLVED_FALSE
    prediction.resolved_at = datetime.now(timezone.utc)
    prediction.final_brier_score = calculate_brier_score(prediction.probability_estimate, outcome)

    forecasts = db.query(Forecast).filter(Forecast.prediction_id == prediction.id).all()
    for forecast in forecasts:
        forecast.brier_score = calculate_brier_score(forecast.probability_estimate, outcome)
        db.add(forecast)

    db.add(prediction)
    db.commit()

    recalculate_all_reputations_for_prediction(db, prediction.id)

    db.refresh(prediction)
    return prediction
