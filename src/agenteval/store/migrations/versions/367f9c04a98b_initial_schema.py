"""initial schema

Revision ID: 367f9c04a98b
Revises:
Create Date: 2024-06-17 15:34:57.176529

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "367f9c04a98b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "run",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "test",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("steps", sa.String(), nullable=False),
        sa.Column("initial_prompt", sa.String(), nullable=True),
        sa.Column("max_turns", sa.Integer(), nullable=False),
        sa.Column("hook", sa.String(), nullable=True),
        sa.Column("start_time", sa.DateTime(), nullable=False),
        sa.Column("end_time", sa.DateTime(), nullable=False),
        sa.Column("run_id", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["run.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "expected",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("conversation", sa.String(), nullable=False),
        sa.Column("test_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["test_id"],
            ["test.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "test_result",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("result", sa.String(), nullable=False),
        sa.Column("reasoning", sa.String(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("messages", sa.String(), nullable=False),
        sa.Column("events", sa.String(), nullable=False),
        sa.Column("evaluator_input_token_count", sa.Integer(), nullable=False),
        sa.Column("evaluator_output_token_count", sa.Integer(), nullable=False),
        sa.Column("test_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["test_id"],
            ["test.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("test_result")
    op.drop_table("expected")
    op.drop_table("test")
    op.drop_table("run")
