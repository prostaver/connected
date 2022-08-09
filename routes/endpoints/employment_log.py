from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db_connection
from pydantic_schemas import employment_log as employment_log_schema
from services import employment_log_service

router = APIRouter(
    prefix="/employment_logs",
    tags={"employment_logs"}
)

@router.get("/", response_model=List[employment_log_schema.EmploymentLog], status_code=status.HTTP_200_OK)
async def get_employment_logs(applicant_id: int, db: Session = Depends(get_db_connection)):
    return employment_log_service.get_employment_logs(db, applicant_id)

@router.get("/{employment_log_id}", response_model=employment_log_schema.EmploymentLog, status_code=status.HTTP_200_OK)
async def get_employment_log(employment_log_id: int, applicant_id: int, db: Session = Depends(get_db_connection)):
    return employment_log_service.get_employment_logs(db, applicant_id, employment_log_id)

@router.post("/", response_model=employment_log_schema.EmploymentLog, status_code=status.HTTP_200_OK)
async def create_employment_logs(employment_log_input: employment_log_schema.CreateEmploymentLog, db: Session = Depends(get_db_connection)):
    return employment_log_service.create_or_update_employment_log(db, employment_log_input)

@router.post("/{employment_log_id}", response_model=employment_log_schema.EmploymentLog, status_code=status.HTTP_200_OK)
async def udpate_employment_logs(employment_log_id: int, employment_log_input: employment_log_schema.CreateEmploymentLog, db: Session = Depends(get_db_connection)):
    return employment_log_service.create_or_update_employment_log(db, employment_log_input, employment_log_id)

@router.delete("/{employment_log_id}", response_model=employment_log_schema.EmploymentLog, status_code=status.HTTP_200_OK)
async def delete_employment_logs(employment_log_id: int, applicant_id: int, db: Session = Depends(get_db_connection)):
    return employment_log_service.delete_employment_log(db, employment_log_id, applicant_id)