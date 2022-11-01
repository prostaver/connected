from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import job_position as model_job_position
from models import job_application as model_job_application
from pydantic_schemas import job_position as job_position_schema


def create_job_position(db: Session, job_position_input: job_position_schema.CreateJobPosition):
    """Creates a job position open for an employer/company."""
    jp_data = model_job_position.JobPosition(
        title=job_position_input.title,
        description=job_position_input.description,
        salary=job_position_input.salary,
        employer_id=job_position_input.employer_id
    )

    db.add(jp_data)
    db.commit()

    return jp_data


def get_job_positions(db: Session, employer_id: int = None, job_position_id: int = None):
    """Retrieves the list of job positions or a single job position if the job position id is specified"""
    if job_position_id:
        job_position_data = db.query(model_job_position.JobPosition).filter(
            model_job_position.JobPosition.id == job_position_id).first()
        if not job_position_data:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"No job position found with id: {job_position_id}")
        return job_position_data

    if employer_id:
        return db.query(model_job_position.JobPosition).filter(
            model_job_position.JobPosition.employer_id == employer_id).all()

    return db.query(model_job_position.JobPosition).all()


def update_jp_status():
    # TODO add status field in job position model before adding logic to this function.
    return


def delete_job_position(db: Session, job_position_id: int, employer_id: int):
    """Deletes the job position with the selected id."""
    job_position = db.query(model_job_position.JobPosition).filter(
        model_job_position.JobPosition.id == job_position_id).first()
    if job_position.employer_id != employer_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            f"You are not authorized to modify the job position with id {job_position_id}")
    db.query(model_job_position.JobPosition).filter(model_job_position.JobPosition.id == job_position_id).delete()
    db.commit()

    return {"message": f"Successfully deleted job position with id: {job_position_id}"}


def get_applied_job_positions_by_applicant(db: Session, applicant_id: int):
    ja_list = db.query(model_job_application.JobApplication).filter(
        model_job_application.JobApplication.applicant_id == applicant_id).all()
    return db.query(model_job_position.JobPosition).filter(
        model_job_position.JobPosition.id.in_(jp.id for jp in ja_list)).all()
