import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Forecast(Base):
    """A single user's probability estimate against an existing Prediction.

    One user can only have one active forecast per prediction — submitting
    again updates the existing row rather than creating a duplicate. This
    keeps the crowd-consensus calculation from being skewed by users who
    forecast the same question repeatedly.
    """

    __tablename__ = "forecasts"
    __table_args__ = (UniqueConstraint("prediction_id", "user_id", name="uq_forecast_user_prediction"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    prediction_id: Mapped[str] = mapped_column(String(36), ForeignKey("predictions.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)

    probability_estimate: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)
    )

    # Set once the parent prediction resolves, so a user's individual
    # accuracy on this question doesn't need to be recomputed from
    # scratch every time their profile is viewed.
    brier_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    prediction = relationship("Prediction", back_populates="forecasts")
    user = relationship("User", back_populates="forecasts")

    def __repr__(self) -> str:  # pragma: no cover - debug helper only
        return f"<Forecast user={self.user_id[:8]} p={self.probability_estimate}>"
