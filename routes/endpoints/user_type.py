from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db_connection
from pydantic_schemas.user_type import UserType
from services import user_type_service

router = APIRouter(
    prefix="/user_types",
    tags={"user_types"}
)

@router.get("/", response_model=List[UserType], status_code=status.HTTP_200_OK)
async def get_user_types(db: Session = Depends(get_db_connection)):
    return user_type_service.get_user_types(db)

@router.get("/{user_type_id}", response_model=UserType, status_code=status.HTTP_200_OK)
async def get_user_type(user_type_id: int, db: Session = Depends(get_db_connection)):
    return user_type_service.get_user_types(db, user_type_id)
