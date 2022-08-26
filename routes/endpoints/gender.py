from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db_connection
from pydantic_schemas.gender import Gender
from services import gender_service

router = APIRouter(
    prefix="/genders",
    tags=["genders"]
)


@router.get("/", response_model=List[Gender], status_code=status.HTTP_200_OK)
async def get_genders(db: Session = Depends(get_db_connection)):
    return gender_service.get_genders(db)


@router.get("/{gender_id}", response_model=Gender, status_code=status.HTTP_200_OK)
async def get_gender(gender_id: int, db: Session = Depends(get_db_connection)):
    return gender_service.get_genders(db, gender_id)
