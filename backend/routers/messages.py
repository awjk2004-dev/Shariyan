from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from auth import get_current_user
from database import get_db
from models import BloodRequest, Message, Notification, User
from schemas import MessageCreate, MessageOut

router = APIRouter()


@router.post("", response_model=MessageOut, status_code=201)
def send_message(payload: MessageCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    recipient = db.get(User, payload.recipient_id)
    if not recipient or recipient.id == user.id:
        raise HTTPException(status_code=400, detail="Invalid recipient")
    if payload.request_id:
        request = db.get(BloodRequest, payload.request_id)
        if not request or (request.requester_id != user.id and request.requester_id != recipient.id):
            raise HTTPException(status_code=403, detail="Message is not related to this request")
    message = Message(sender_id=user.id, **payload.model_dump())
    db.add(message)
    db.add(Notification(user_id=recipient.id, title="رسالة جديدة", body=f"لديك رسالة جديدة من {user.full_name}.", link=f"message.html?recipient={user.id}"))
    db.commit()
    db.refresh(message)
    return message


@router.get("/{user_id}", response_model=list[MessageOut])
def conversation(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not db.get(User, user_id) or user_id == user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    query = select(Message).where(
        or_(
            and_(Message.sender_id == user.id, Message.recipient_id == user_id),
            and_(Message.sender_id == user_id, Message.recipient_id == user.id),
        )
    ).order_by(Message.created_at.asc())
    messages = list(db.scalars(query))
    for message in messages:
        if message.recipient_id == user.id and message.read_at is None:
            message.read_at = datetime.now(timezone.utc)
    db.commit()
    return messages
