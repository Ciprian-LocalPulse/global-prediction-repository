from fastapi import FastAPI

from app.config import get_settings
from app.routers import auth, forecasts, leaderboard, oracle, predictions, users

settings = get_settings()

app = FastAPI(
    title=settings.project_name,
    description=(
        "An open, auditable repository of falsifiable predictions across "
        "climate, public health, AI and technological risk, resource "
        "management, and geopolitical stability."
    ),
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(predictions.router)
app.include_router(forecasts.router)
app.include_router(oracle.router)
app.include_router(leaderboard.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": settings.project_name}
