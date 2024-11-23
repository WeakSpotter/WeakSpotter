from datetime import timedelta

from app.database import SessionDep
from app.models.user import User
from app.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select

router = APIRouter()


@router.post("/auth/login/", tags=["auth"])
def login(
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # Search for the user by username
    user = session.exec(select(User).where(User.username == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate a JWT token
    access_token = create_access_token(
        {"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


# OAuth2PasswordBearer to validate tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login/")


@router.post("/users/", tags=["users"])
def register_user(username: str, password: str, session: SessionDep):
    # Check if the user already exists
    existing_user = session.exec(select(User).where(User.username == username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password
    hashed_password = hash_password(password)

    # Create a new user
    user = User(username=username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "User registered successfully",
        "user": {"id": user.id, "username": user.username},
    }


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dependency to verify the JWT token and retrieve the connected user.
    """
    payload = decode_access_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username


@router.get("/users/me", tags=["users"])
def read_current_user(current_user: str = Depends(get_current_user)):
    """
    Returns the information of the connected user.
    """
    return {"username": current_user}
