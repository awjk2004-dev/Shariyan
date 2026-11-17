import os
import secrets

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import select
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, hash_password, verify_password
from database import get_db
from models import User
from schemas import Token, UserCreate, UserOut

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=UserOut, status_code=201)
@limiter.limit(os.getenv("RATE_LIMIT", "60/minute"))
def register(request: Request, payload: UserCreate, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == payload.email)):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(**payload.model_dump(exclude={"password"}), password_hash=hash_password(payload.password), email_verified=True)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
@limiter.limit(os.getenv("RATE_LIMIT", "60/minute"))
def login(request: Request, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username))
    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return Token(access_token=create_access_token(user.id))


@router.post("/bootstrap-admin", response_model=UserOut)
def bootstrap_admin(x_admin_bootstrap_token: str = Header(default=""), db: Session = Depends(get_db)):
    expected = os.getenv("ADMIN_BOOTSTRAP_TOKEN")
    if not expected or not secrets.compare_digest(x_admin_bootstrap_token, expected):
        raise HTTPException(status_code=403, detail="Invalid bootstrap token")
    if db.scalar(select(User).where(User.is_admin.is_(True))):
        raise HTTPException(status_code=409, detail="An admin already exists")
    user = db.scalar(select(User).order_by(User.id))
    if not user:
        raise HTTPException(status_code=404, detail="Create a user first")
    user.is_admin = True
    user.email_verified = True
    db.commit()
    db.refresh(user)
    return user


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
