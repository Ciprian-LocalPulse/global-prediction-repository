from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.enums import Domain, PredictionStatus
from app.database import get_db
from app.dependencies import get_current_user
from app.models.forecast import Forecast
from app.models.prediction import Prediction
from app.models.user import User
from app.schemas.prediction import PredictionCreate, PredictionRead, PredictionWithConsensus
from app.services.crowd_wisdom import crowd_consensus

router = APIRouter(prefix="/predictions", tags=["predictions"])


def _with_consensus(db: Session, prediction: Prediction) -> PredictionWithConsensus:
    forecasts = db.query(Forecast).filter(Forecast.prediction_id == prediction.id).all()
    return PredictionWithConsensus(
        **PredictionRead.model_validate(prediction).model_dump(),
        crowd_consensus_probability=crowd_consensus(forecasts),
        forecast_count=len(forecasts),
    )


@router.post("", response_model=PredictionRead, status_code=201)
def create_prediction(
    payload: PredictionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prediction = Prediction(
        creator_id=current_user.id,
        domain=payload.domain,
        hypothesis=payload.hypothesis,
        resolution_criteria=payload.resolution_criteria,
        resolution_date=payload.resolution_date,
        probability_estimate=payload.probability_estimate,
        rationale=payload.rationale,
    )
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


@router.get("", response_model=list[PredictionWithConsensus])
def list_predictions(
    domain: Domain | None = None,
    status_filter: PredictionStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db),
):
    query = db.query(Prediction)
    if domain is not None:
        query = query.filter(Prediction.domain == domain)
    if status_filter is not None:
        query = query.filter(Prediction.status == status_filter)

    predictions = (
        query.order_by(Prediction.created_at.desc()).offset(offset).limit(limit).all()
    )
    return [_with_consensus(db, p) for p in predictions]


@router.get("/{prediction_id}", response_model=PredictionWithConsensus)
def get_prediction(prediction_id: str, db: Session = Depends(get_db)):
    prediction = db.get(Prediction, prediction_id)
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return _with_consensus(db, prediction)
