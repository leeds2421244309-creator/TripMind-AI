"""add RULE to todo_source enum

Revision ID: 7a2c3f0e9b8d
Revises: 5f95a178965d
Create Date: 2026-09-02
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7a2c3f0e9b8d"
down_revision = "5f95a178965d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "travel_todos",
        "source",
        existing_type=sa.Enum("AI", "USER", name="todosource"),
        type_=sa.Enum("AI", "USER", "RULE", name="todosource"),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "travel_todos",
        "source",
        existing_type=sa.Enum("AI", "USER", "RULE", name="todosource"),
        type_=sa.Enum("AI", "USER", name="todosource"),
        existing_nullable=False,
    )
