"""add in-app notifications

Revision ID: 0002_notifications
Revises: 0001_initial
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_notifications"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("notifications", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("title", sa.String(160), nullable=False), sa.Column("body", sa.String(500), nullable=False), sa.Column("link", sa.String(255), nullable=True), sa.Column("read_at", sa.DateTime(), nullable=True), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])


def downgrade():
    op.drop_table("notifications")
