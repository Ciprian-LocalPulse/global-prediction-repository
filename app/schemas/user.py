from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import UserRole


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(min_length=8)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: EmailStr
    role: UserRole
    global_accuracy_score: float
    resolved_forecast_count: int
    created_at: datetime


class UserPublic(BaseModel):
    """Slimmer view used when a user appears as someone else's creator/forecaster."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    global_accuracy_score: float


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
