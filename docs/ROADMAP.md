# Roadmap

## Phase 1 — MVP (this repository)

The current state of the codebase:

- [x] Database schema for users, predictions, and forecasts, with Alembic
      migrations
- [x] Authentication (registration, login, JWT-protected endpoints)
- [x] Core forecasting mechanic: create a prediction, submit a
      probability estimate against it, revise it while the prediction is
      still open
- [x] Manual resolution workflow, restricted to the Oracle/Admin role
- [x] Brier score calculation on resolution
- [x] Reputation engine (rolling global accuracy score per user)
- [x] Crowd consensus aggregation (simple average, reputation-weighted
      average once there's enough data)
- [x] Leaderboard endpoint
- [x] Seed set of predictions across all five launch domains

Not yet built, and intentionally out of scope for this repository:
a frontend, a public embeddable API, and automated resolution.

## Phase 2 — Community & Analysis Engine

Planned, not yet started:

- Public-facing frontend (dashboards, prediction detail pages showing how
  the crowd consensus moved over time, user profile pages)
- Historical consensus tracking — right now the API only exposes the
  *current* crowd consensus; storing a time series of how it moved as
  forecasts came in is needed for the "consensus over time" visualization
  the roadmap calls for
- Commenting and rationale discussion threads attached to individual
  predictions
- Public launch, including onboarding for university researchers
- Refinement of the leaderboard's minimum-resolved-forecast threshold,
  ideally toward a confidence-interval-based approach (see
  `docs/METHODOLOGY.md`)

## Phase 3 — Automation & Global Scale

Longer-term, dependent on Phase 2 usage patterns validating the core
mechanics first:

- Public read API for media outlets to embed live probabilities
- AI models as first-class Forecaster accounts, competing alongside human
  users on the same leaderboard
- Automated Oracle resolution against verified external data feeds (WHO,
  WMO, World Bank, USDA, and similar), for predictions whose resolution
  criteria can be tied to a structured, machine-readable source
- Rate limiting, abuse detection, and other production-hardening work
  appropriate for a fully public, high-traffic API

## Deliberately deferred questions

A few product questions are left open rather than pre-decided, since
they're better answered with real usage data than guessed at up front:

- Should reputation decay over time, so a strong track record from years
  ago counts less than recent accuracy? The current implementation
  treats all resolved history equally.
- Should there be a mechanism for disputing a resolution before it's
  final, rather than only before-the-fact ambiguity handling?
- What's the right way to handle predictions that get *more* forecasts
  than expected on a sensitive or politically contested topic — is
  reputation-weighting sufficient, or does that need additional
  moderation tooling?

These are noted here so they don't get silently decided by default
behavior; any of them is a reasonable place for a future contributor to
start a design discussion.
