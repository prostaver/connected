from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db_connection
from services import applicant_service

router = APIRouter(
    prefix="/applicants",
    tags={"applicants"}
)

@router.get("/")
async def get_applicants(db: Session = Depends(get_db_connection)):
    return applicant_service.get_applicants(db)

@router.get("/{applicant_id}")
async def get_applicant(applicant_id: int, db: Session = Depends(get_db_connection)):
    return applicant_service.get_applicants(db, applicant_id)

@router.delete("/{applicant_id}")
async def delete_applicant(applicant_id: int, db: Session = Depends(get_db_connection)):
    return applicant_service.delete_applicant(db, applicant_id)