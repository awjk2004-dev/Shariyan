"""Align timestamps and indexes with application queries.

Revision ID: 0003_query_indexes
Revises: 0002_notifications
"""
from alembic import op
import sqlalchemy as sa

revision = "0003_query_indexes"
down_revision = "0002_notifications"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_blood_requests_status", table_name="blood_requests")
    op.drop_index("ix_messages_sender_id", table_name="messages")
    op.drop_index("ix_messages_recipient_id", table_name="messages")
    op.drop_index("ix_notifications_user_id", table_name="notifications")

    for table in ("users", "blood_requests", "messages", "notifications"):
        op.alter_column(
            table,
            "created_at",
            existing_type=sa.DateTime(),
            existing_nullable=True,
            existing_server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            server_default=sa.func.now(),
        )

    op.create_index(
        "ix_blood_requests_status_urgent_created",
        "blood_requests",
        ["status", "urgent", "created_at"],
    )
    op.create_index(
        "ix_messages_sender_recipient_created",
        "messages",
        ["sender_id", "recipient_id", "created_at"],
    )
    op.create_index(
        "ix_messages_recipient_sender_created",
        "messages",
        ["recipient_id", "sender_id", "created_at"],
    )
    op.create_index(
        "ix_notifications_user_created",
        "notifications",
        ["user_id", "created_at"],
    )


def downgrade():
    op.drop_index("ix_notifications_user_created", table_name="notifications")
    op.drop_index("ix_messages_recipient_sender_created", table_name="messages")
    op.drop_index("ix_messages_sender_recipient_created", table_name="messages")
    op.drop_index("ix_blood_requests_status_urgent_created", table_name="blood_requests")

    for table in ("users", "blood_requests", "messages", "notifications"):
        op.alter_column(
            table,
            "created_at",
            existing_type=sa.DateTime(),
            existing_nullable=False,
            existing_server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
            server_default=sa.func.now(),
        )

    op.create_index("ix_notifications_user_id", "notifications", ["user_id"])
    op.create_index("ix_messages_recipient_id", "messages", ["recipient_id"])
    op.create_index("ix_messages_sender_id", "messages", ["sender_id"])
    op.create_index("ix_blood_requests_status", "blood_requests", ["status"])
    op.create_index("ix_users_email", "users", ["email"])
