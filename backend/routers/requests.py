from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models import BloodRequest, BloodType, Donor, Notification, RequestStatus, User
from ..schemas import RequestCreate, RequestOut

router = APIRouter()


@router.post("", response_model=RequestOut, status_code=201)
def create_request(payload: RequestCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    request = BloodRequest(requester_id=user.id, **payload.model_dump())
    db.add(request)
    db.commit()
    db.refresh(request)
    donor_users = db.scalars(select(User).join(Donor).where(Donor.blood_type == payload.blood_type, Donor.available.is_(True), User.city.ilike(f"%{payload.city}%"), User.id != user.id)).all()
    for donor_user in donor_users:
        db.add(Notification(user_id=donor_user.id, title="طلب دم قريب منك", body=f"يوجد طلب فصيلة {payload.blood_type} في مدينة {payload.city}.", link=f"requests.html?id={request.id}"))
    db.commit()
    return request


@router.get("", response_model=list[RequestOut])
def list_requests(blood_type: BloodType | None = None, city: str | None = None, status: RequestStatus = RequestStatus.OPEN, db: Session = Depends(get_db)):
    query = select(BloodRequest).where(BloodRequest.status == status)
    if blood_type:
        query = query.where(BloodRequest.blood_type == blood_type)
    if city:
        query = query.where(BloodRequest.city.ilike(f"%{city}%"))
    return list(db.scalars(query.order_by(BloodRequest.urgent.desc(), BloodRequest.created_at.desc())))


@router.patch("/{request_id}/cancel", response_model=RequestOut)
def cancel_request(request_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    request = db.get(BloodRequest, request_id)
    if not request or request.requester_id != user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    request.status = RequestStatus.CANCELLED
    db.commit()
    db.refresh(request)
    return request
