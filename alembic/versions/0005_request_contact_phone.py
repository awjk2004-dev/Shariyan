"""Add an optional public contact phone to blood requests.

Revision ID: 0005_request_contact_phone
Revises: 0004_donor_search_index
"""
from alembic import op
import sqlalchemy as sa

revision = "0005_request_contact_phone"
down_revision = "0004_donor_search_index"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "blood_requests",
        sa.Column("contact_phone", sa.String(length=30), nullable=True),
    )


def downgrade():
    op.drop_column("blood_requests", "contact_phone")
