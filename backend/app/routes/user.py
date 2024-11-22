import os
import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import select
from app.models.user import User
from app.database import SessionDep
from app.security import hash_password, verify_password  # Import depuis security.py


router = APIRouter()

# Configuration pour JWT
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_default_key")
ALGORITHM = "HS256"

# OAuth2PasswordBearer pour valider les tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


@router.post("/users/")
def register_user(username: str, password: str, session: SessionDep):
    # Vérifier si l'utilisateur existe déjà
    existing_user = session.exec(select(User).where(User.username == username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hacher le mot de passe
    hashed_password = hash_password(password)

    # Créer un nouvel utilisateur
    user = User(username=username, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "User registered successfully", "user": {"id": user.id, "username": user.username}}

@router.post("/auth/login/")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: SessionDep = Depends(),
):
    # Rechercher l'utilisateur par nom d'utilisateur
    user = session.exec(select(User).where(User.username == form_data.username)).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Générer un token JWT
    access_token = jwt.encode(
        {"sub": user.username, "exp": datetime.utcnow() + timedelta(hours=1)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dépendance pour vérifier le token JWT et récupérer l'utilisateur connecté.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/users/me")
def read_current_user(current_user: str = Depends(get_current_user)):
    """
    Retourne les informations de l'utilisateur connecté.
    """
    return {"username": current_user}