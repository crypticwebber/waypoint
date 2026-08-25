from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED,
    summary="Create an account",
    description="Registers a new student or instructor account and immediately returns a "
                "JWT so the frontend can move straight into the onboarding survey without "
                "a second login round-trip.",
)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    user = models.User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(str(user.id))
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@router.post(
    "/login", response_model=schemas.Token,
    summary="Log in",
    description="Exchanges an email + password for a JWT access token.",
)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(str(user.id))
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@router.get(
    "/me", response_model=schemas.UserOut,
    summary="Get the logged-in user",
)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user
