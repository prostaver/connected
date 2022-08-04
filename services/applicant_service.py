from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import applicant as model_applicant
from pydantic_schemas import applicant as applicant_schema

def get_applicants(db: Session, applicant_id: int = None):
    """Retrieves the list of applicants or a single applicant if the applicant id is specified"""
    if applicant_id:
        applicant = db.query(model_applicant.Applicant).filter(model_applicant.Applicant.id == applicant_id).first()
        if not applicant:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"No applicant found with id: {applicant_id}")
        return applicant

    return db.query(model_applicant.Applicant).all()

def create_applicant(db: Session, user_id: int = None):
    """Creates or updates the applicant details for the user."""
    applicant_data = get_applicant_by_user_id(db, user_id)

    if applicant_data:
        return applicant_data
    
    applicant_data = model_applicant.Applicant(
        user_id = user_id
    )

    db.add(applicant_data)
    db.commit()

    return applicant_data

def get_applicant_by_user_id(db: Session, user_id: int):
    """Retrieves the applicant data based on the related user id."""
    return db.query(model_applicant.Applicant).filter(model_applicant.Applicant.user_id == user_id).first()

def delete_applicant(db: Session, applicant_id: int):
    """Deletes the applicant data with the selected id."""
    db.query(model_applicant.Applicant).filter(model_applicant.Applicant.id == applicant_id).delete()
    db.commit()

    return {"message": f"Successfuly deleted applicant detail with applicant id: {applicant_id}"}