import time

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from .hash_func import verify_password
from . import user_service

SECRET_KEY = "c42dff633cc265f6444335d6094f87e309854b7c92f9b290c7d102d7a342adbc"
ALGORITHM = "HS256"


def create_auth_token(db: Session, email: str, password: str):
    user = user_service.get_user_by_email(db, email)
    if not verify_password(password, user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Incorrect username or password", {"WWW-Authenticate": "Bearer"})

    payload = {
        "user_email": user.email,
        "expiration": time.time() + 300000
    }

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}


def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return decoded_token if decoded_token["expiration"] >= time.time() else None
    except ValueError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token.", {"WWW-Authenticate": "Bearer"})
