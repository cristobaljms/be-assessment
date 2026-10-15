"""Create customers table.

Revision ID: 20261014_0001
Revises:
Create Date: 2026-10-14
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261014_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE",
                "PENDING",
                "BLOCKED",
                name="customer_status",
                native_enum=False,
                create_constraint=True,
                length=16,
            ),
            server_default="PENDING",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_customers_email"),
    )
    op.create_index("ix_customers_email", "customers", ["email"], unique=False)
    op.create_index("ix_customers_status", "customers", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_customers_status", table_name="customers")
    op.drop_index("ix_customers_email", table_name="customers")
    op.drop_table("customers")
