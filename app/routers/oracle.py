from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.core.exceptions import InvalidResolutionError
from app.database import get_db
from app.dependencies import get_current_user
from app.models.prediction import Prediction
from app.models.user import User
from app.schemas.prediction import PredictionRead, PredictionResolve
from app.services.resolution import resolve_prediction

router = APIRouter(prefix="/oracle", tags=["oracle"])


def require_oracle(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in (UserRole.ORACLE, UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only users with the Oracle or Admin role can resolve predictions",
        )
    return current_user


@router.post("/predictions/{prediction_id}/resolve", response_model=PredictionRead)
def resolve(
    prediction_id: str,
    payload: PredictionResolve,
    db: Session = Depends(get_db),
    _: User = Depends(require_oracle),
):
    prediction = db.get(Prediction, prediction_id)
    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")

    try:
        return resolve_prediction(
            db,
            prediction,
            outcome=payload.outcome if not payload.ambiguous else None,
            ambiguous=payload.ambiguous,
        )
    except InvalidResolutionError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
