from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..auth import require_admin
from ..database import get_db
from ..models import BloodRequest, Donor, RequestStatus, User
from ..schemas import RequestOut, UserCityUpdate, UserOut

router = APIRouter()


@router.get("/stats")
def stats(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return {
        "users": db.scalar(select(func.count()).select_from(User)) or 0,
        "donors": db.scalar(select(func.count()).select_from(Donor)) or 0,
        "requests": db.scalar(select(func.count()).select_from(BloodRequest)) or 0,
    }


@router.get("/reports/overview")
def overview_report(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    status_counts = dict(db.execute(select(BloodRequest.status, func.count()).group_by(BloodRequest.status)).all())
    blood_type_counts = dict(db.execute(select(BloodRequest.blood_type, func.count()).group_by(BloodRequest.blood_type)).all())
    city_counts = dict(db.execute(select(BloodRequest.city, func.count()).group_by(BloodRequest.city).order_by(func.count().desc()).limit(10)).all())
    return {
        "totals": {
            "users": db.scalar(select(func.count()).select_from(User)) or 0,
            "donors": db.scalar(select(func.count()).select_from(Donor)) or 0,
            "requests": db.scalar(select(func.count()).select_from(BloodRequest)) or 0,
        },
        "requests_by_status": {key.value: value for key, value in status_counts.items()},
        "requests_by_blood_type": {key.value: value for key, value in blood_type_counts.items()},
        "requests_by_city": city_counts,
        "urgent_open_requests": db.scalar(select(func.count()).select_from(BloodRequest).where(BloodRequest.urgent.is_(True), BloodRequest.status == RequestStatus.OPEN)) or 0,
    }


@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return list(db.scalars(select(User).order_by(User.created_at.desc())))


@router.patch("/users/{user_id}/city", response_model=UserOut)
def update_user_city(user_id: int, payload: UserCityUpdate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.city = payload.city.strip()
    db.commit()
    db.refresh(user)
    return user


@router.get("/requests", response_model=list[RequestOut])
def list_all_requests(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    return list(db.scalars(select(BloodRequest).order_by(BloodRequest.created_at.desc())))


@router.patch("/requests/{request_id}/status", response_model=RequestOut)
def update_request_status(request_id: int, status: RequestStatus, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    request = db.get(BloodRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    request.status = status
    db.commit()
    db.refresh(request)
    return request


@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.get(User, user_id)
    if not user or user.id == admin.id:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()


@router.patch("/donors/{donor_id}/availability", response_model=bool)
def update_donor_availability(donor_id: int, available: bool, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    donor = db.get(Donor, donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    donor.available = available
    db.commit()
    return donor.available


@router.delete("/donors/{donor_id}", status_code=204)
def delete_donor(donor_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    donor = db.get(Donor, donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    db.delete(donor)
    db.commit()
