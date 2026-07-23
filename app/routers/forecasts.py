from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.enums import PredictionStatus
from app.database import get_db
from app.dependencies import get_current_user
from app.models.forecast import Forecast
from app.models.prediction import Prediction
from app.models.user import User
from app.schemas.forecast import ForecastCreate, ForecastRead

router = APIRouter(prefix="/predictions/{prediction_id}/forecasts", tags=["forecasts"])


@router.post("", response_model=ForecastRead, status_code=201)
def submit_forecast(
    prediction_id: str,
    payload: ForecastCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prediction = db.get(Prediction, prediction_id)
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")

    if prediction.status != PredictionStatus.OPEN:
        raise HTTPException(
            status_code=409,
            detail=f"Prediction is {prediction.status.value} and no longer accepting forecasts",
        )

    existing = (
        db.query(Forecast)
        .filter(Forecast.prediction_id == prediction_id, Forecast.user_id == current_user.id)
        .first()
    )

    if existing is not None:
        # Update in place — see the note on the Forecast model. A user
        # revising their estimate as new information comes in is normal
        # forecasting behavior, not something to penalize with duplicate
        # rows.
        existing.probability_estimate = payload.probability_estimate
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing

    forecast = Forecast(
        prediction_id=prediction_id,
        user_id=current_user.id,
        probability_estimate=payload.probability_estimate,
    )
    db.add(forecast)
    db.commit()
    db.refresh(forecast)
    return forecast


@router.get("", response_model=list[ForecastRead])
def list_forecasts(prediction_id: str, db: Session = Depends(get_db)):
    prediction = db.get(Prediction, prediction_id)
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")

    return (
        db.query(Forecast)
        .filter(Forecast.prediction_id == prediction_id)
        .order_by(Forecast.timestamp.desc())
        .all()
    )
