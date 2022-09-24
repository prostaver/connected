from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import job_application as model_job_application
from pydantic_schemas import job_application as job_application_schema


def create_job_application(db: Session, ja_input: job_application_schema.CreateJobApplication):
    ja_data = model_job_application.JobApplication(
        applicant_id=ja_input.applicant_id,
        job_position_id=ja_input.job_position_id,
        status=ja_input.status
    )

    db.add(ja_data)
    db.commit()

    return ja_data


def update_job_application(db: Session, ja_input: job_application_schema.CreateJobApplication, ja_id: int):
    ja_data = get_job_application(db, ja_id)
    ja_data.applicant_id = ja_input.applicant_id
    ja_data.job_position_id = ja_input.job_position_id
    ja_data.status = ja_input.status

    db.add(ja_data)
    db.commit()

    return ja_data


def get_job_applications(db: Session):
    jas = db.query(model_job_application.JobApplication).all()
    return jas


def get_job_application(db: Session, ja_id: int):
    ja = db.query(model_job_application.JobApplication).filter(model_job_application.JobApplication.id == ja_id).first()
    if not ja:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No Job Application found with id {ja_id}")
    return ja


def delete_job_application(db: Session, ja_id: int):
    ja = db.query(model_job_application.JobApplication).filter(model_job_application.JobApplication.id == ja_id).first()
    if not ja:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"No Job Application found with id {ja_id}")

    db.delete(ja)
    db.commit()

    return {"message": f"Successfully deleted job application with id: {ja_id}"}
