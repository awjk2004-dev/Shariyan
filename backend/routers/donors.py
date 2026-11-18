from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from auth import get_current_user
from database import get_db
from models import BloodType, Donor, User
from schemas import DonorCreate, DonorOut, LeaderboardEntry

router = APIRouter()


@router.post("/me", response_model=DonorOut, status_code=201)
def register_donor(payload: DonorCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    donor = db.scalar(select(Donor).where(Donor.user_id == user.id).options(joinedload(Donor.user)))
    if donor:
        donor.blood_type = payload.blood_type
        donor.available = payload.available
        donor.last_donation = payload.last_donation
    else:
        donor = Donor(user_id=user.id, **payload.model_dump())
        db.add(donor)
    db.commit()
    db.refresh(donor)
    return donor


@router.get("/me", response_model=DonorOut | None)
def get_my_donor_profile(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.scalar(
        select(Donor).where(Donor.user_id == user.id).options(joinedload(Donor.user))
    )


@router.get("", response_model=list[DonorOut])
def list_donors(blood_type: BloodType | None = None, city: str | None = None, db: Session = Depends(get_db)):
    query = select(Donor).join(Donor.user).options(joinedload(Donor.user)).where(Donor.available.is_(True))
    if blood_type:
        query = query.where(Donor.blood_type == blood_type)
    if city:
        query = query.where(User.city.ilike(f"%{city}%"))
    return list(db.scalars(query.order_by(Donor.id.desc())).unique())


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
def donor_leaderboard(db: Session = Depends(get_db)):
    donors = list(db.scalars(
        select(Donor).join(Donor.user).options(joinedload(Donor.user)).where(Donor.available.is_(True))
    ).unique())
    donors.sort(key=lambda donor: (
        donor.last_donation is not None,
        donor.last_donation or donor.user.created_at,
        donor.user.created_at,
    ), reverse=True)
    return [
        {
            "rank": index,
            "score": 100 if donor.last_donation else 70,
            "blood_type": donor.blood_type,
            "last_donation": donor.last_donation,
            "user": donor.user,
        }
        for index, donor in enumerate(donors[:10], start=1)
    ]
