from fastapi import APIRouter, status, Depends
from pydantic_schemas import user as user_schema
from sqlalchemy.orm import Session
from typing import List

from config.database import getDbConection
from services import user_service

router = APIRouter(
    prefix = "/users"
)

@router.get("/", response_model=List[user_schema.User], status_code=status.HTTP_200_OK)
def getUsers(db: Session=Depends(getDbConection)):
    users = user_service.getUsers(db=db)
    return users

@router.get("/{user_id}", response_model=user_schema.User, status_code=status.HTTP_200_OK)
def getUser(user_id:int, db: Session=Depends(getDbConection)):
    user = user_service.getUsers(user_id=user_id, db=db)
    return user

@router.post('/', response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def createUser(user_schema:user_schema.CreateUser, db: Session=Depends(getDbConection)):
    new_user = user_service.createOrUpdateUser(user_schema=user_schema, db=db)

    return new_user

@router.post('/{user_id}', response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def updateUser(user_id: int, user_schema:user_schema.CreateUser, db: Session=Depends(getDbConection)):
    updated_user = user_service.createOrUpdateUser(user_id=user_id, user_schema=user_schema, db=db)

    return updated_user
