"""initial schema: users, predictions, forecasts

Revision ID: 0001
Revises:
Create Date: 2026-07-23

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_role_enum = sa.Enum("forecaster", "oracle", "admin", name="userrole")
domain_enum = sa.Enum(
    "climate_environment",
    "public_health",
    "ai_tech_risk",
    "resource_management",
    "geopolitical_stability",
    name="domain",
)
prediction_status_enum = sa.Enum(
    "open", "closed", "resolved_true", "resolved_false", "ambiguous", name="predictionstatus"
)


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("username", sa.String(length=64), nullable=False, unique=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role_enum, nullable=False, server_default="forecaster"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("global_accuracy_score", sa.Float(), nullable=False, server_default="50.0"),
        sa.Column("resolved_forecast_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_users_username", "users", ["username"])
    op.create_index("ix_users_email", "users", ["email"])

    op.create_table(
        "predictions",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("creator_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("domain", domain_enum, nullable=False),
        sa.Column("hypothesis", sa.Text(), nullable=False),
        sa.Column("resolution_criteria", sa.Text(), nullable=False),
        sa.Column("resolution_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("probability_estimate", sa.Float(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False, server_default=""),
        sa.Column("status", prediction_status_enum, nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("final_brier_score", sa.Float(), nullable=True),
    )
    op.create_index("ix_predictions_domain", "predictions", ["domain"])
    op.create_index("ix_predictions_status", "predictions", ["status"])

    op.create_table(
        "forecasts",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column(
            "prediction_id", sa.String(length=36), sa.ForeignKey("predictions.id"), nullable=False
        ),
        sa.Column("user_id", sa.String(length=36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("probability_estimate", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("brier_score", sa.Float(), nullable=True),
        sa.UniqueConstraint("prediction_id", "user_id", name="uq_forecast_user_prediction"),
    )


def downgrade() -> None:
    op.drop_table("forecasts")
    op.drop_index("ix_predictions_status", table_name="predictions")
    op.drop_index("ix_predictions_domain", table_name="predictions")
    op.drop_table("predictions")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")

    prediction_status_enum.drop(op.get_bind(), checkfirst=True)
    domain_enum.drop(op.get_bind(), checkfirst=True)
    user_role_enum.drop(op.get_bind(), checkfirst=True)
