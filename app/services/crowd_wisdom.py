"""
Aggregating individual forecasts into a single "crowd consensus"
probability.

Two aggregation modes are supported:

- Simple average: every forecast counts equally. This is the classic
  "wisdom of crowds" approach and is what we default to, because it's
  transparent and hard to game.
- Reputation-weighted average: forecasts from users with a stronger track
  record (higher global_accuracy_score) count for more. This tends to
  outperform the simple average once there's enough resolved history to
  make the weights meaningful, but it's also the mechanism most
  vulnerable to a bad early calibration, so it's opt-in rather than the
  default in Phase 1.
"""

from app.models.forecast import Forecast

MIN_WEIGHT = 1.0  # floor so a low-reputation user still has some voice


def simple_average(forecasts: list[Forecast]) -> float | None:
    if not forecasts:
        return None
    total = sum(f.probability_estimate for f in forecasts)
    return round(total / len(forecasts), 2)


def reputation_weighted_average(forecasts: list[Forecast]) -> float | None:
    if not forecasts:
        return None

    weighted_sum = 0.0
    weight_total = 0.0
    for f in forecasts:
        weight = max(f.user.global_accuracy_score, MIN_WEIGHT)
        weighted_sum += f.probability_estimate * weight
        weight_total += weight

    if weight_total == 0:
        return simple_average(forecasts)

    return round(weighted_sum / weight_total, 2)


def crowd_consensus(forecasts: list[Forecast], weighted: bool = True) -> float | None:
    """Entry point used by the routers. Falls back to a simple average
    for fewer than 3 forecasts, since weighting doesn't mean much with a
    tiny sample and can make a single confident-but-wrong early forecaster
    look more authoritative than they should.
    """
    if weighted and len(forecasts) >= 3:
        return reputation_weighted_average(forecasts)
    return simple_average(forecasts)
