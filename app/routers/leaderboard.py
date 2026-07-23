from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("", response_model=list[UserRead])
def leaderboard(
    min_resolved: int = Query(
        default=3,
        ge=0,
        description="Minimum number of resolved forecasts required to appear on the leaderboard.",
    ),
    limit: int = Query(default=25, le=100),
    db: Session = Depends(get_db),
):
    # The min_resolved floor exists so a single lucky forecast can't put
    # someone at the top of the leaderboard on day one.
    return (
        db.query(User)
        .filter(User.resolved_forecast_count >= min_resolved)
        .order_by(User.global_accuracy_score.desc())
        .limit(limit)
        .all()
    )
