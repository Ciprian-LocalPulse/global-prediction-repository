# API Reference

The full interactive reference is always available at `/docs` (Swagger UI)
or `/redoc` once the service is running — this document is a narrative
walkthrough of the main endpoints and how they're meant to be used
together, not a substitute for the generated schema.

Base URL in local development: `http://localhost:8000`

## Authentication

### `POST /auth/register`

Creates a new account. Body:

```json
{
  "username": "jsmith",
  "email": "jsmith@example.com",
  "password": "at-least-8-characters"
}
```

Returns the created user (without the password hash). New accounts start
with `global_accuracy_score: 50.0` and `role: "forecaster"`.

### `POST /auth/login`

Standard OAuth2 password flow — form-encoded, not JSON:

```
username=jsmith&password=at-least-8-characters
```

Returns `{"access_token": "...", "token_type": "bearer"}`. Send this token
as `Authorization: Bearer <token>` on any endpoint that requires auth.

## Users

### `GET /users/me`

Requires auth. Returns the caller's own profile, including their current
reputation.

### `GET /users/{user_id}`

Public. Returns another user's profile by ID.

## Predictions

### `POST /predictions`

Requires auth. Creates a new prediction, owned by the calling user.

```json
{
  "domain": "climate_environment",
  "hypothesis": "Global average surface temperature will exceed 1.5C above baseline in 2027.",
  "resolution_criteria": "Per the WMO annual state-of-the-climate report for 2027.",
  "resolution_date": "2027-12-31T00:00:00Z",
  "probability_estimate": 38,
  "rationale": "Based on current warming trajectory and ENSO forecasts."
}
```

Valid values for `domain`: `climate_environment`, `public_health`,
`ai_tech_risk`, `resource_management`, `geopolitical_stability`.

`resolution_date` must be in the future. `probability_estimate` must be
between 0 and 100. The new prediction starts in `open` status.

### `GET /predictions`

Public. Lists predictions, newest first. Query parameters:

- `domain` — filter by domain
- `status` — filter by status (`open`, `closed`, `resolved_true`,
  `resolved_false`, `ambiguous`)
- `limit` — default 50, max 200
- `offset` — for pagination

Each result includes `crowd_consensus_probability` and `forecast_count`,
computed live from the attached forecasts.

### `GET /predictions/{prediction_id}`

Public. Same shape as a single item from the list endpoint above.

## Forecasts

### `POST /predictions/{prediction_id}/forecasts`

Requires auth. Submits (or updates) the caller's probability estimate on
a prediction.

```json
{ "probability_estimate": 42 }
```

Only allowed while the prediction's status is `open`. Submitting again
updates your existing forecast rather than creating a second one — see
`docs/ARCHITECTURE.md` for why.

### `GET /predictions/{prediction_id}/forecasts`

Public. Lists every individual forecast on a prediction, most recent
first. Once a prediction resolves, each forecast in this list will also
carry its own `brier_score`.

## Oracle

### `POST /oracle/predictions/{prediction_id}/resolve`

Requires the `oracle` or `admin` role (returns 403 otherwise — there is
no self-service way to become an oracle; see `docs/ARCHITECTURE.md`).

```json
{ "outcome": true }
```

or, for a prediction whose resolution criteria turned out not to be
cleanly applicable:

```json
{ "outcome": true, "ambiguous": true }
```

(`outcome` is ignored when `ambiguous` is `true`.)

Resolving a prediction is a one-time action — attempting to resolve an
already-resolved prediction returns 409. On success, every attached
forecast gets scored and every involved user's reputation is
recalculated in the same operation.

## Leaderboard

### `GET /leaderboard`

Public. Returns users ranked by `global_accuracy_score`, descending.

- `min_resolved` — minimum number of resolved forecasts required to
  appear (default 3, set to 0 to see everyone)
- `limit` — default 25, max 100

## Health check

### `GET /health`

Returns `{"status": "ok", "service": "Global Prediction Repository"}`.
Useful for container orchestration liveness checks.
