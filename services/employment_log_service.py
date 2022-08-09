from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import employment_log as model_employment_log
from pydantic_schemas import employment_log as employment_log_schema

def create_or_update_employment_log(db: Session, employment_log_input: employment_log_schema.CreateEmploymentLog, employment_log_id: int = None):
    """Create or update an employment log."""
    employment_log_data = None
    if employment_log_id:
        employment_log_data = db.query(model_employment_log.EmploymentLog).filter(model_employment_log.EmploymentLog.id == employment_log_id)
        if not employment_log_data:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Could not update. No employment log found with id: {employment_log_id}")
        employment_log_data.company_name = employment_log_input.company_name
        employment_log_data.position = employment_log_input.position
        employment_log_data.tenure = employment_log_input.tenure
        employment_log_data.is_current = employment_log_input.is_current
        employment_log_data.applicant_id = employment_log_input.applicant_id
        employment_log_data.job_position_id = employment_log_input.job_position_id

    employment_log_data = model_employment_log.EmploymentLog(
        company_name = employment_log_input.company_name,
        position = employment_log_input.position,
        tenure = employment_log_input.tenure,
        is_current = employment_log_input.is_current,
        applicant_id = employment_log_input.applicant_id,
        job_position_id = employment_log_input.job_position_id
    )

    db.add(employment_log_data)
    db.commit()

    return employment_log_data

def get_employment_logs(db: Session, applicant_id: int, employment_log_id: int = None):
    """Get a single or list of employment log of the current applicant."""
    if employment_log_id:
        employment_log = db.query(model_employment_log.EmploymentLog).filter(model_employment_log.EmploymentLog.applicant_id == applicant_id, model_employment_log.EmploymentLog.id == employment_log_id)
        if not employment_log:
            return HTTPException(status.HTTP_404_NOT_FOUND, f"No employment log found with id: {employment_log_id} for applicant id: {applicant_id}")
        return employment_log
    return db.query(model_employment_log.EmploymentLog).filter(model_employment_log.EmploymentLog.applicant_id == applicant_id).all()

def delete_employment_log(db: Session, employment_log_id: int, applicant_id: int):
    """Deletes the employment log with the selected id."""
    employment_log = db.query(model_employment_log.EmploymentLog).filter(model_employment_log.EmploymentLog.applicant_id == applicant_id, model_employment_log.EmploymentLog.id == employment_log_id).first()
    if not employment_log:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"You are not authorized to modify the employment log with id {employment_log_id}")

    db.query(model_employment_log.EmploymentLog).filter(model_employment_log.EmploymentLog.id == employment_log_id).delete()
    db.commit()

    return {"message": f"Successfully deleted employment log with id: {employment_log_id}"}