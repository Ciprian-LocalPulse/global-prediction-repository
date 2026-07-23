# Architecture

This document explains how the pieces fit together and, more importantly,
why they're arranged this way. It's meant for someone who already knows
FastAPI and SQLAlchemy and wants to get oriented in this specific codebase
quickly, not as a general tutorial on either.

## Layering

The codebase follows a fairly conventional three-layer split:

```
routers/     HTTP concerns only: parsing requests, checking auth, calling
             a service, shaping the response. No business logic lives here.

services/    Business logic. Brier scoring, crowd-consensus aggregation,
             reputation recalculation, and the resolution workflow that
             ties them together. These functions take SQLAlchemy sessions
             and ORM objects directly — they're not trying to be
             storage-agnostic, since realistically this project has one
             database and pretending otherwise would just add
             indirection without benefit.

models/      SQLAlchemy ORM models, one file per table. Kept intentionally
             thin — no business logic on the models themselves beyond a
             __repr__ for debugging.

schemas/     Pydantic request/response models. Validation that's purely
             about shape (e.g., "probability must be 0-100", "resolution
             date must be in the future") lives here, since Pydantic runs
             before a request even reaches a router. Validation that
             depends on database state (e.g., "this prediction must be
             open") lives in the service or router layer instead.
```

The rule of thumb: if two different routers would need to duplicate a
piece of logic, it belongs in `services/`. If it's about parsing a
specific request or shaping a specific response, it stays in the router.

## Why the resolution flow is centralized

`app/services/resolution.py` is the one place where scoring a prediction,
scoring every attached forecast, and triggering reputation updates all
happen together, in a fixed order, inside one function
(`resolve_prediction`). This was a deliberate choice rather than
scattering the steps across the oracle router.

The reasoning: resolution is the one operation in this system where
partial completion would actually be dangerous. If a prediction's status
flipped to "resolved" but the attached forecasts never got scored, every
downstream reputation number would quietly be wrong, and nothing in the
API would signal that anything had gone wrong. Keeping all three steps
inside a single function, inside a single database transaction, means
there's no window where the system is in a half-resolved state that
looks complete from the outside.

## Why Brier scoring and reputation are separate services

`app/services/brier.py` only knows about one thing: given a probability
and an outcome, what's the squared error. It has no concept of a user,
a prediction, or a database session. `app/services/reputation.py` is the
layer above it that knows how to pull a user's forecast history and turn
a list of Brier scores into a single rolling accuracy number.

Splitting these apart made the test suite substantially easier to write.
`test_brier_score.py` can assert on the math directly, with plain floats
and booleans, without touching a database at all. `test_reputation.py`
exercises the full path through the API instead, because that's the
layer where the interesting integration behavior (does resolving a
prediction actually update the right users?) lives.

## Crowd consensus: why the weighting only kicks in at 3+ forecasts

`app/services/crowd_wisdom.py` falls back to a simple average when a
prediction has fewer than three forecasts, and only switches to
reputation-weighted averaging once there are at least three. This isn't
an arbitrary number — it's there because reputation-weighting with one or
two forecasters just means "whichever of them has a slightly higher
score wins," which isn't really wisdom-of-crowds behavior at all, it's
noise dressed up as a weighted average. Three is the smallest sample
where averaging starts to mean something.

## Why forecasts update in place instead of accumulating

The `Forecast` model has a unique constraint on `(prediction_id,
user_id)`. Submitting a new forecast on a question you've already
forecasted updates your existing row rather than inserting a new one.
Real forecasters revise their estimates constantly as new information
arrives — that's supposed to happen, and penalizing it (or letting it
silently duplicate rows and skew the crowd average) would push people
toward stating an opinion once and defending it, which is the opposite
of the behavior this whole project is trying to reward.

## Authentication

Nothing unusual: OAuth2 password flow, bcrypt-hashed passwords, short-
lived HS256 JWTs carrying just the user ID as the subject claim. There's
no refresh-token flow yet — access tokens expire after
`ACCESS_TOKEN_EXPIRE_MINUTES` (default 60) and the user logs in again.
That's a reasonable trade-off for an MVP; a refresh-token flow is a
natural addition once there's a frontend session to keep alive across
longer usage.

## Roles

Three roles exist on `User.role`: `forecaster` (default), `oracle`, and
`admin`. There is deliberately no public endpoint for granting yourself
the oracle role — it's a database-level promotion, done by whoever is
running the deployment. This matches the roadmap's Phase 1 description of
the Oracle as "trusted human experts" rather than something users opt
into themselves.

## What's intentionally not here yet

- **No automated resolution against external data feeds.** That's a
  Phase 3 roadmap item (see `docs/ROADMAP.md`), and building it before
  the manual resolution flow has been exercised by real predictions would
  be solving a problem before it's clear what shape it actually takes.
- **No frontend.** This repository is the backend only, per the current
  scope. `app/main.py` exposes interactive OpenAPI docs at `/docs`, which
  is sufficient for exploring and testing the API without a UI.
- **No rate limiting or abuse protection.** Fine for an MVP behind a
  reverse proxy with its own protections; worth adding before this goes
  fully public in Phase 2.
