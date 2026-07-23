# Contributing

Thanks for considering contributing to the Global Prediction Repository.
This is early-stage software — the backend described in this repository
covers the Phase 1 scope from the project roadmap, and there's a lot of
room for people who want to help shape what comes next.

## Ways to help that don't require writing code

- **Propose new predictions.** Good predictions are harder to write than
  they look — the resolution criteria need to be specific enough that
  reasonable people wouldn't disagree about the outcome once it happens.
  If you have domain expertise in climate science, epidemiology, AI
  policy, resource economics, or geopolitics, well-scoped prediction
  proposals are genuinely valuable.
- **Stress-test existing resolution criteria.** If you can find a way a
  current seed prediction's criteria could resolve ambiguously, that's
  useful feedback — open an issue describing the ambiguity.
- **Review the methodology.** `docs/METHODOLOGY.md` lays out the
  statistical reasoning behind the scoring system. If something there is
  wrong, or there's a better-established approach we should be using
  instead, that kind of critique is welcome.

## Setting up a development environment

Follow the "Getting started" section in the main `README.md`. In short:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
pytest -v
```

Tests run against an in-memory SQLite database, so you don't need
Postgres running locally to contribute code.

## Code style

- Type hints on function signatures, including return types.
- Keep business logic in `app/services/`, not in routers — see
  `docs/ARCHITECTURE.md` for the reasoning.
- New service functions should have a corresponding unit or integration
  test. Untested business logic in a project built around trustworthy
  scoring is a contradiction in terms.
- Docstrings and inline comments should explain *why*, not narrate
  *what* — the code already says what it does.

## Submitting changes

1. Open an issue first for anything beyond a small fix, so the approach
   can be discussed before significant work goes into it.
2. Keep pull requests focused on one change. A PR that fixes a bug and
   also refactors an unrelated module is harder to review and harder to
   revert if something goes wrong.
3. Make sure `pytest -v` passes locally before opening a PR — CI will
   run the same suite.
4. Reference the roadmap phase your change belongs to, if applicable
   (see `docs/ROADMAP.md`), so reviewers have context on scope.

## Reporting bugs or scoring discrepancies

If you believe a specific prediction was scored incorrectly, please
include the prediction ID, the expected Brier score calculation, and
what the API actually returned. Scoring bugs are treated as high
priority, since the entire point of this project is that the numbers can
be trusted.
