import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import Domain, PredictionStatus
from app.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    creator_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    domain: Mapped[Domain] = mapped_column(Enum(Domain), nullable=False, index=True)

    hypothesis: Mapped[str] = mapped_column(Text, nullable=False)
    resolution_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    resolution_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # The creator's own initial probability estimate. Distinct from the
    # crowd consensus, which is computed from all Forecast rows.
    probability_estimate: Mapped[float] = mapped_column(Float, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, default="")

    status: Mapped[PredictionStatus] = mapped_column(
        Enum(PredictionStatus), default=PredictionStatus.OPEN, nullable=False, index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Populated once the prediction resolves. This is the *creator's*
    # Brier score on their own initial estimate — the crowd's aggregate
    # score is derived separately from the Forecast rows in the
    # reputation service, since each forecaster's score is individual.
    final_brier_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    creator = relationship("User", back_populates="predictions_created")
    forecasts = relationship(
        "Forecast", back_populates="prediction", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper only
        return f"<Prediction {self.id[:8]} [{self.status.value}] {self.hypothesis[:40]!r}>"
