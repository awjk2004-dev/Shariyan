from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from  models import BloodType, RequestStatus


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone: str = Field(min_length=7, max_length=30)
    city: str = Field(min_length=2, max_length=100)
    blood_type: BloodType | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    email: EmailStr
    phone: str
    city: str
    is_admin: bool
    email_verified: bool


class UserCityUpdate(BaseModel):
    city: str = Field(min_length=2, max_length=100)


class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_name: str
    city: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DonorCreate(BaseModel):
    blood_type: BloodType
    available: bool = True
    last_donation: datetime | None = None


class DonorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    blood_type: BloodType
    available: bool
    last_donation: datetime | None
    user: UserPublic


class LeaderboardEntry(BaseModel):
    rank: int
    score: int
    blood_type: BloodType
    last_donation: datetime | None
    user: UserPublic


class RequestCreate(BaseModel):
    patient_name: str = Field(min_length=2, max_length=120)
    blood_type: BloodType
    city: str = Field(min_length=2, max_length=100)
    hospital: str = Field(min_length=2, max_length=180)
    contact_phone: str | None = Field(default=None, min_length=7, max_length=30)
    units: int = Field(default=1, ge=1, le=20)
    urgent: bool = True
    notes: str | None = Field(default=None, max_length=1000)


class RequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    patient_name: str
    blood_type: BloodType
    city: str
    hospital: str
    contact_phone: str | None
    units: int
    urgent: bool
    notes: str | None
    status: RequestStatus
    created_at: datetime


class PublicRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    blood_type: BloodType
    city: str
    hospital: str
    contact_phone: str | None
    units: int
    urgent: bool
    status: RequestStatus
    created_at: datetime


class MessageCreate(BaseModel):
    recipient_id: int
    request_id: int | None = None
    content: str = Field(min_length=1, max_length=2000)


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sender_id: int
    recipient_id: int
    request_id: int | None
    content: str
    created_at: datetime
    read_at: datetime | None


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    body: str
    link: str | None
    read_at: datetime | None
    created_at: datetime
