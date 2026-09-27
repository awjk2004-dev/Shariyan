"""initial schema

Revision ID: 0001_initial
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None
blood_type = sa.Enum("A_POSITIVE", "A_NEGATIVE", "B_POSITIVE", "B_NEGATIVE", "AB_POSITIVE", "AB_NEGATIVE", "O_POSITIVE", "O_NEGATIVE", name="bloodtype")
request_status = sa.Enum("OPEN", "FULFILLED", "CANCELLED", name="requeststatus")


def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("full_name", sa.String(120), nullable=False), sa.Column("email", sa.String(255), nullable=False), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("phone", sa.String(30), nullable=False), sa.Column("city", sa.String(100), nullable=False), sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()), sa.Column("email_verified", sa.Boolean(), nullable=False, server_default=sa.false()), sa.Column("verification_token", sa.String(128), nullable=True), sa.Column("verification_expires_at", sa.DateTime(), nullable=True), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()), sa.UniqueConstraint("email"), sa.UniqueConstraint("verification_token"))
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_city", "users", ["city"])
    op.create_table("donors", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("blood_type", blood_type, nullable=False), sa.Column("available", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("last_donation", sa.DateTime(), nullable=True), sa.UniqueConstraint("user_id"))
    op.create_index("ix_donors_blood_type", "donors", ["blood_type"])
    op.create_index("ix_donors_available", "donors", ["available"])
    op.create_table("blood_requests", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("requester_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("patient_name", sa.String(120), nullable=False), sa.Column("blood_type", blood_type, nullable=False), sa.Column("city", sa.String(100), nullable=False), sa.Column("hospital", sa.String(180), nullable=False), sa.Column("units", sa.Integer(), nullable=False, server_default="1"), sa.Column("urgent", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("notes", sa.Text(), nullable=True), sa.Column("status", request_status, nullable=False), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()))
    op.create_index("ix_blood_requests_blood_type", "blood_requests", ["blood_type"])
    op.create_index("ix_blood_requests_city", "blood_requests", ["city"])
    op.create_index("ix_blood_requests_status", "blood_requests", ["status"])
    op.create_table("messages", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("sender_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("recipient_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("request_id", sa.Integer(), sa.ForeignKey("blood_requests.id", ondelete="SET NULL"), nullable=True), sa.Column("content", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()), sa.Column("read_at", sa.DateTime(), nullable=True))
    op.create_index("ix_messages_sender_id", "messages", ["sender_id"])
    op.create_index("ix_messages_recipient_id", "messages", ["recipient_id"])
    op.create_index("ix_messages_request_id", "messages", ["request_id"])


def downgrade():
    op.drop_table("messages")
    op.drop_table("blood_requests")
    op.drop_table("donors")
    op.drop_table("users")
