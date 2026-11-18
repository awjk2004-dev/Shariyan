from datetime import datetime
from enum import Enum
from typing import Optional   # ← أضف هذا السطر

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class BloodType(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class RequestStatus(str, Enum):
    OPEN = "open"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(30))
    city: Mapped[str] = mapped_column(String(100), index=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verification_token: Mapped[Optional[str]] = mapped_column(String(128), unique=True, nullable=True)  # ← تعديل
    verification_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)          # ← تعديل
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    donor_profile: Mapped["Donor"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")


class Donor(Base):
    __tablename__ = "donors"
    __table_args__ = (Index("ix_donors_blood_type_available", "blood_type", "available"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    blood_type: Mapped[BloodType] = mapped_column(SqlEnum(BloodType), index=True)
    available: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    last_donation: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)   # ← تعديل
    user: Mapped[User] = relationship(back_populates="donor_profile")


class BloodRequest(Base):
    __tablename__ = "blood_requests"
    __table_args__ = (Index("ix_blood_requests_status_urgent_created", "status", "urgent", "created_at"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    requester_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    patient_name: Mapped[str] = mapped_column(String(120))
    blood_type: Mapped[BloodType] = mapped_column(SqlEnum(BloodType), index=True)
    city: Mapped[str] = mapped_column(String(100), index=True)
    hospital: Mapped[str] = mapped_column(String(180))
    units: Mapped[int] = mapped_column(Integer, default=1)
    urgent: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)                    # ← تعديل
    status: Mapped[RequestStatus] = mapped_column(SqlEnum(RequestStatus), default=RequestStatus.OPEN)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        Index("ix_messages_sender_recipient_created", "sender_id", "recipient_id", "created_at"),
        Index("ix_messages_recipient_sender_created", "recipient_id", "sender_id", "created_at"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    request_id: Mapped[Optional[int]] = mapped_column(ForeignKey("blood_requests.id", ondelete="SET NULL"), nullable=True, index=True)  # ← تعديل
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)         # ← تعديل


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (Index("ix_notifications_user_created", "user_id", "created_at"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(160))
    body: Mapped[str] = mapped_column(String(500))
    link: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)              # ← تعديل
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)         # ← تعديل
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
