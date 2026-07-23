"""
Drops and recreates all tables directly via SQLAlchemy metadata.

This is a development convenience, not a substitute for Alembic. Use it
when you want to wipe a local scratch database quickly; use Alembic
migrations for anything that resembles a real deployment, including CI.

Usage:
    python scripts/reset_db.py --yes-i-am-sure
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import models  # noqa: F401,E402 - registers models on Base.metadata
from app.database import Base, engine  # noqa: E402


def main():
    if "--yes-i-am-sure" not in sys.argv:
        print("This will drop every table in the configured database.")
        print("Re-run with --yes-i-am-sure if that's what you want.")
        return

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Dropped and recreated all tables.")


if __name__ == "__main__":
    main()
