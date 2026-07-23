from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.enums import Domain, PredictionStatus
from app.schemas.user import UserPublic


class PredictionCreate(BaseModel):
    domain: Domain
    hypothesis: str = Field(min_length=20, max_length=2000)
    resolution_criteria: str = Field(min_length=20, max_length=4000)
    resolution_date: datetime
    probability_estimate: float = Field(ge=0, le=100)
    rationale: str = Field(default="", max_length=8000)

    @field_validator("resolution_date")
    @classmethod
    def resolution_date_must_be_future(cls, value: datetime) -> datetime:
        # Normalize naive datetimes to UTC before comparing, so callers
        # that forget to attach a timezone don't slip through.
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        if value <= datetime.now(timezone.utc):
            raise ValueError("resolution_date must be in the future")
        return value


class PredictionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    domain: Domain
    hypothesis: str
    resolution_criteria: str
    resolution_date: datetime
    probability_estimate: float
    rationale: str
    status: PredictionStatus
    created_at: datetime
    resolved_at: datetime | None
    final_brier_score: float | None
    creator: UserPublic


class PredictionWithConsensus(PredictionRead):
    """PredictionRead plus the live crowd-aggregated probability.

    Kept as a separate schema rather than folding consensus into
    PredictionRead so that list endpoints, which don't need the extra
    aggregation query, stay cheap.
    """

    crowd_consensus_probability: float | None
    forecast_count: int


class PredictionResolve(BaseModel):
    outcome: bool  # True -> Resolved_True, False -> Resolved_False
    ambiguous: bool = False  # set True if the resolution criteria could not be cleanly applied
