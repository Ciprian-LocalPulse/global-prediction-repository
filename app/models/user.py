import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import UserRole
from app.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.FORECASTER, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Reputation. Recomputed by app.services.reputation whenever a
    # prediction this user forecasted on gets resolved.
    global_accuracy_score: Mapped[float] = mapped_column(Float, default=50.0)
    resolved_forecast_count: Mapped[int] = mapped_column(Integer, default=0)

    predictions_created = relationship(
        "Prediction", back_populates="creator", cascade="all, delete-orphan"
    )
    forecasts = relationship(
        "Forecast", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper only
        return f"<User {self.username} score={self.global_accuracy_score:.1f}>"
