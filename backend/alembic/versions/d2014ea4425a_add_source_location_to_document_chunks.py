"""add source location to document chunks

Revision ID: d2014ea4425a
Revises: c260e93c43c4
Create Date: 2026-11-02 12:07:44.125900
"""

from alembic import op
import sqlalchemy as sa


revision = "d2014ea4425a"
down_revision = "c260e93c43c4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "document_chunks",
        sa.Column(
            "source_location",
            sa.String(length=500),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column(
        "document_chunks",
        "source_location",
    )