from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db_connection
from pydantic_schemas import qualification as qualification_schema
from services import qualification_service

router = APIRouter(
    prefix="/qualifications",
    tags=["qualifications"]
)


@router.get("/", response_model=List[qualification_schema.Qualification], status_code=status.HTTP_200_OK)
async def get_qualifications(applicant_id: int, db: Session = Depends(get_db_connection)):
    return qualification_service.get_qualifications(db, applicant_id)


@router.get("/{qualification_id}", response_model=qualification_schema.Qualification, status_code=status.HTTP_200_OK)
async def get_qualification(qualification_id: int, applicant_id: int, db: Session = Depends(get_db_connection)):
    return qualification_service.get_qualifications(db, applicant_id, qualification_id)


@router.post("/", response_model=qualification_schema.Qualification, status_code=status.HTTP_200_OK)
async def create_qualification(qualification_input: qualification_schema.CreateQualification,
                               db: Session = Depends(get_db_connection)):
    return qualification_service.create_or_update_qualification(db, qualification_input)


@router.post("/{qualification_id}", response_model=qualification_schema.Qualification, status_code=status.HTTP_200_OK)
async def update_qualification(qualification_id: int, qualification_input: qualification_schema.CreateQualification,
                               db: Session = Depends(get_db_connection)):
    return qualification_service.create_or_update_qualification(db, qualification_input, qualification_id)


@router.delete("/{qualification_id}", status_code=status.HTTP_200_OK)
async def delete_qualification(qualification_id: int, applicant_id: int, db: Session = Depends(get_db_connection)):
    return qualification_service.delete_qualification(db, qualification_id, applicant_id)
