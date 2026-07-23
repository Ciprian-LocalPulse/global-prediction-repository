
# Global Prediction Repository (GPR)
![Global Prediction Repository](assets/global_prediction.png)
An open, auditable ledger of falsifiable predictions across the domains that
shape the next decade — climate, public health, artificial intelligence,
resource security, and geopolitical stability. The GPR exists because most
forecasting happens in places where nobody has to answer for being wrong:
op-eds, cable news panels, conference keynotes. This project tries something
different. Every prediction gets a resolution date, an explicit criterion for
judging it, and a Brier score once the world tells us the answer.

This repository contains the backend service that makes that possible: a
FastAPI application backed by PostgreSQL, with the scoring and reputation
logic that turns raw forecasts into a track record.

## Why a repository like this matters

Forecasters are rarely graded. Pundits move from one confident claim to the
next without anyone checking the last one. The GPR is an attempt to close
that loop. It does three things that most commentary does not:

- **Keeps score.** Every resolved prediction gets a Brier score, a standard
  measure of forecast accuracy that penalizes overconfidence.
- **Aggregates independent judgment.** Decades of research on the "wisdom of
  crowds" — going back to Galton's ox-weighing crowd in 1907, and more
  recently formalized in Philip Tetlock's forecasting tournaments — shows
  that averaging many independent, reasonably informed estimates usually
  beats any single expert.
- **Makes track records portable.** A user's accuracy history lives with
  their account, not with whichever platform they happened to post on.

## What's in this repository

```
global-prediction-repository/
├── app/                  FastAPI application (models, schemas, routers, services)
├── alembic/               Database migrations
├── tests/                 pytest test suite
├── scripts/                Database seeding and maintenance scripts
├── data/seed/               Seed predictions used for local development
├── docs/                  Architecture notes, methodology, API reference
├── docker-compose.yml     Local Postgres + API stack
└── requirements.txt
```

## Getting started

### Prerequisites

- Python 3.11 or later
- PostgreSQL 14 or later (or Docker, if you'd rather not install it locally)

### Local setup

```bash
git clone https://github.com/Ciprian-LocalPulse/global-prediction-repository.git
cd global-prediction-repository

python -m venv .venv
source .venv/bin/activate        # .venv\Scripts\activate on Windows

pip install -r requirements.txt

cp .env.example .env             # then edit DATABASE_URL and SECRET_KEY
```

### Running with Docker (recommended for local development)

```bash
docker compose up --build
```

This brings up a Postgres instance and the API together. The API will be
available at `http://localhost:8000`, with interactive docs at
`http://localhost:8000/docs`.

### Running without Docker

```bash
# apply migrations
alembic upgrade head

# load the seed predictions (optional, but useful for exploring the API)
python scripts/seed_database.py

# start the API
uvicorn app.main:app --reload
```

### Running the tests

```bash
pytest -v
```

The test suite runs against an in-memory SQLite database, so it doesn't
require a running Postgres instance. It covers the prediction lifecycle,
the Brier score calculation, the crowd-wisdom aggregation, and the
reputation engine.

## Core concepts

**Prediction** — A single hypothesis with a resolution date and explicit
resolution criteria, created by a user or an AI model. Example: "Global
average surface temperature will exceed 1.5°C above the pre-industrial
baseline for calendar year 2027, per the WMO annual state-of-the-climate
report."

**Forecast** — An individual probability estimate (0–100%) submitted against
an existing prediction. A single prediction can accumulate forecasts from
many users; the API aggregates these into a crowd consensus probability.

**Brier score** — The squared error between a forecaster's stated
probability and the eventual binary outcome. Lower is better; 0 is a
perfect forecast, 1 is the worst possible one, 0.25 is what you'd get from
a coin flip on a 50/50 question.

**Reputation** — A rolling accuracy score derived from a user's resolved
predictions, used to weight their forecasts more heavily in the crowd
consensus calculation.

**Oracle** — The role responsible for resolving a prediction once its
resolution date has passed, using the resolution criteria specified at
creation time. In Phase 1 this is a human moderator action; the roadmap
calls for automated resolution against verified data feeds in Phase 3.

See `docs/METHODOLOGY.md` for the full statistical reasoning behind the
scoring and weighting choices, and `docs/ARCHITECTURE.md` for how the
service is put together.

## Project status

This is the Phase 1 (MVP) backend described in the project roadmap: schema,
authentication, the core forecasting mechanic, and the resolution/scoring
logic, seeded with a starting set of predictions across climate, public
health, and AI risk. A frontend and the public API for media embedding are
future phases — see `docs/ROADMAP.md`.

## Contributing

Contributions are welcome, particularly around resolution criteria for
existing predictions, additional domain categories, and edge cases in the
scoring logic. See `docs/CONTRIBUTING.md`.

## License

MIT. See `LICENSE`.
>>>>>>> 726d8ee4fa167a1a8e8ad93683f0e48a5089fda4
