from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserPublic


class ForecastCreate(BaseModel):
    probability_estimate: float = Field(ge=0, le=100)


class ForecastRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    prediction_id: str
    probability_estimate: float
    timestamp: datetime
    brier_score: float | None
    user: UserPublic
