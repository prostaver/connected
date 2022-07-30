from fastapi import APIRouter, status, Depends
from pydantic_schemas import user as user_schema
from sqlalchemy.orm import Session
from typing import List

from routes.endpoints.login import oauth2_scheme
from config.database import get_db_connection
from services import user_service

router = APIRouter(
    prefix = "/users",
    tags={"users"}
)

@router.get("/", response_model=List[user_schema.User], status_code=status.HTTP_200_OK)
async def get_users(db: Session=Depends(get_db_connection)):
    users = user_service.get_users(db=db)
    return users

@router.get("/{user_id}", response_model=user_schema.User, status_code=status.HTTP_200_OK)
async def get_user(user_id:int, db: Session=Depends(get_db_connection)):
    user = user_service.get_users(db=db, user_id=user_id)
    return user

@router.post('/', response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
async def create_user(user_schema:user_schema.CreateUser, db: Session=Depends(get_db_connection)):
    new_user = user_service.create_or_update_user(db=db, user_input=user_schema)
    return new_user

@router.post('/{user_id}', response_model=user_schema.User, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user_schema:user_schema.CreateUser, db: Session=Depends(get_db_connection)):
    updated_user = user_service.create_or_update_user(db=db, user_id=user_id, user_input=user_schema)
    return updated_user

@router.get("/current/", status_code=status.HTTP_200_OK)
async def get_users_copy(token: str = Depends(oauth2_scheme), db: Session=Depends(get_db_connection)):
    payload = user_service.decode_token(token)
    user = user_service.get_user_by_email(db=db, email=payload.get("user_email"))
    return user
