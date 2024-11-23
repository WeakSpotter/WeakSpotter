from datetime import timedelta

from app.database import SessionDep
from app.models.user import User, UserCreate
from app.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    UserDep,
    create_access_token,
    hash_password,
    verify_password,
)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

router = APIRouter()


@router.post("/auth/login/", tags=["auth"])
def login(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(
        {"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", tags=["users"])
def register_user(user_create: UserCreate, session: SessionDep):
    existing_user = session.exec(
        select(User).where(User.username == user_create.username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user_create.password)

    user = User(username=user_create.username, hashed_password=hashed_password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "User registered successfully",
        "user": {"id": user.id, "username": user.username},
        "access_token": create_access_token(
            {"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        ),
    }


@router.get("/users/me", tags=["users"])
def read_current_user(current_user: UserDep):
    """
    Returns the information of the connected user.
    """
    return {"username": current_user.username}
