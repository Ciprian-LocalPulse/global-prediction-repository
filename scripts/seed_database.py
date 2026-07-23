"""
Populates the database with a starting set of predictions, per the Phase 1
roadmap goal of launching with a seed set of high-quality predictions in
the climate, health, and AI risk categories (and, here, resource
management and geopolitical stability as well, since the schema already
supports all five launch domains).

Usage:
    python scripts/seed_database.py

Safe to re-run: it checks for an existing seed account and skips creating
duplicate predictions if that account already has some.
"""

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal  # noqa: E402
from app.models.prediction import Prediction  # noqa: E402
from app.models.user import User  # noqa: E402
from app.security import hash_password  # noqa: E402

SEED_FILE = Path(__file__).resolve().parent.parent / "data" / "seed" / "seed_predictions.json"
SEED_USERNAME = "gpr-seed-bot"


def get_or_create_seed_user(db) -> User:
    user = db.query(User).filter(User.username == SEED_USERNAME).first()
    if user is not None:
        return user

    user = User(
        username=SEED_USERNAME,
        email="seed-bot@globalpredictionrepository.org",
        hashed_password=hash_password("not-a-real-login-account"),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created seed account '{SEED_USERNAME}' ({user.id})")
    return user


def load_seed_predictions() -> list[dict]:
    with open(SEED_FILE, encoding="utf-8") as f:
        return json.load(f)


def main():
    db = SessionLocal()
    try:
        seed_user = get_or_create_seed_user(db)

        existing_count = (
            db.query(Prediction).filter(Prediction.creator_id == seed_user.id).count()
        )
        if existing_count > 0:
            print(
                f"Seed account already has {existing_count} predictions attached. "
                "Skipping to avoid duplicates."
            )
            return

        records = load_seed_predictions()
        now = datetime.now(timezone.utc)

        for record in records:
            prediction = Prediction(
                creator_id=seed_user.id,
                domain=record["domain"],
                hypothesis=record["hypothesis"],
                resolution_criteria=record["resolution_criteria"],
                resolution_date=now + timedelta(days=record["resolution_date_days_from_now"]),
                probability_estimate=record["probability_estimate"],
                rationale=record["rationale"],
            )
            db.add(prediction)

        db.commit()
        print(f"Loaded {len(records)} seed predictions across {SEED_FILE.name}.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
