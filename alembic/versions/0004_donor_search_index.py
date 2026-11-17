"""Index donor search filters.

Revision ID: 0004_donor_search_index
Revises: 0003_query_indexes
"""
from alembic import op

revision = "0004_donor_search_index"
down_revision = "0003_query_indexes"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        "ix_donors_blood_type_available",
        "donors",
        ["blood_type", "available"],
    )


def downgrade():
    op.drop_index("ix_donors_blood_type_available", table_name="donors")
