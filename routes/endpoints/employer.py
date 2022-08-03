from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db_connection
from pydantic_schemas import employer as employer_schema
from services import employer_service

router = APIRouter(
    prefix="/employer",
    tags={"employer"}
    # dependencies=Depends(token)
)

@router.get("/", response_model=List[employer_schema.Employer], status_code=status.HTTP_200_OK)
async def get_employers(db: Session = Depends(get_db_connection)):
    return employer_service.get_employers(db)

@router.get("/{employer_id}", response_model=employer_schema.Employer, status_code=status.HTTP_200_OK)
async def get_employer(employer_id: int, db: Session = Depends(get_db_connection)):
    return employer_service.get_employers(db, employer_id)

@router.delete("/{employer_id}", status_code=status.HTTP_200_OK)
async def delete_employer(employer_id: int, db: Session = Depends(get_db_connection)):
    return employer_service.delete_employer(db, employer_id)
