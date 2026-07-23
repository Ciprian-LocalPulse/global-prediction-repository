import enum


class Domain(str, enum.Enum):
    """The five domains the roadmap calls out for the initial launch.

    Kept as a closed enum rather than a free-text field on purpose: it
    keeps the leaderboard and dashboard queries simple, and it forces new
    domains to be a deliberate decision rather than something that drifts
    in through inconsistent user input.
    """

    CLIMATE_ENVIRONMENT = "climate_environment"
    PUBLIC_HEALTH = "public_health"
    AI_TECH_RISK = "ai_tech_risk"
    RESOURCE_MANAGEMENT = "resource_management"
    GEOPOLITICAL_STABILITY = "geopolitical_stability"


class PredictionStatus(str, enum.Enum):
    OPEN = "open"                    # accepting forecasts
    CLOSED = "closed"                # past resolution date, awaiting oracle action
    RESOLVED_TRUE = "resolved_true"
    RESOLVED_FALSE = "resolved_false"
    AMBIGUOUS = "ambiguous"          # resolution criteria could not be applied cleanly


class UserRole(str, enum.Enum):
    FORECASTER = "forecaster"
    ORACLE = "oracle"
    ADMIN = "admin"


RESOLVED_STATUSES = {
    PredictionStatus.RESOLVED_TRUE,
    PredictionStatus.RESOLVED_FALSE,
}
