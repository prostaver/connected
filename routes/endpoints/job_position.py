from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .user import get_current_user
from config.database import get_db_connection
from pydantic_schemas import job_position as job_position_schema, user as user_schema
from services import employer_service, job_position_service

router = APIRouter(
    prefix="/job_positions",
    tags=["job_positions"]
)


@router.get("/", response_model=List[job_position_schema.JobPosition], status_code=status.HTTP_200_OK)
async def get_job_positions(db: Session = Depends(get_db_connection)):
    job_positions = job_position_service.get_job_positions(db)
    return job_positions


@router.get("/by_current_user", response_model=List[job_position_schema.JobPosition], status_code=status.HTTP_200_OK)
async def get_job_positions_by_current_user(db: Session = Depends(get_db_connection),
                                            user: user_schema.User = Depends(get_current_user)):
    employer = employer_service.get_employer_by_user_id(db, user.id)
    job_positions = job_position_service.get_job_positions(db, employer.id)
    return job_positions


@router.get("/{job_position_id}", response_model=job_position_schema.JobPosition, status_code=status.HTTP_200_OK)
async def get_job_position(job_position_id: int, db: Session = Depends(get_db_connection),
                           user: user_schema.User = Depends(get_current_user)):
    employer = employer_service.get_employer_by_user_id(db, user.id)
    job_position = job_position_service.get_job_positions(db, employer.id, job_position_id)
    return job_position


@router.post("/", response_model=job_position_schema.JobPosition, status_code=status.HTTP_201_CREATED)
async def create_job_position(job_position_input: job_position_schema.CreateJobPosition, employer_id: int,
                              db: Session = Depends(get_db_connection)):
    job_position = job_position_service.create_job_position(db, job_position_input, employer_id)
    return job_position


@router.delete("/{job_position_id}", status_code=status.HTTP_200_OK)
async def delete_job_position(job_position_id: int, employer_id: int, db: Session = Depends(get_db_connection)):
    return job_position_service.delete_job_position(db, job_position_id, employer_id)