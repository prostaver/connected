from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import qualification as model_qualification
from pydantic_schemas import qualification as qualification_schema

def create_or_update_qualification(db: Session, qualifiction_input: qualification_schema.CreateQualification, qualification_id: int = None):
    """Create or update an applicant qualification."""
    qualification_data = None
    if qualification_id:
        qualification_data = db.query(model_qualification.Qualification).filter(model_qualification.Qualification.id == qualification_id).first()
        if not qualification_data:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Could not update. No qualification found with id: {qualification_id}")
        qualification_data.details = qualifiction_input.details
        qualification_data.acquirement_date = qualifiction_input.acquirement_date
        qualification_data.applicant_id = qualifiction_input.applicant_id
    else:
        qualification_data = model_qualification.Qualification(
            details = qualifiction_input.details,
            acquirement_date = qualifiction_input.acquirement_date,
            applicant_id = qualifiction_input.applicant_id,
        )

    db.add(qualification_data)
    db.commit()

    return qualification_data

def get_qualifications(db: Session, applicant_id: int, qualification_id: int = None):
    """Get a single or list of qualifications of the current applicant."""
    if qualification_id:
        qualification = db.query(model_qualification.Qualification).filter(model_qualification.Qualification.applicant_id == applicant_id, model_qualification.Qualification.id == qualification_id)
        if not qualification:
            return HTTPException(status.HTTP_404_NOT_FOUND, f"No applicant qualification found with id: {qualification_id} for applicant id: {applicant_id}")
        return qualification
    return db.query(model_qualification.Qualification).filter(model_qualification.Qualification.applicant_id == applicant_id).all()

def delete_qualification(db: Session, qualification_id: int, applicant_id: int):
    """Deletes the applicant qualification with the selected id."""
    qualification = db.query(model_qualification.Qualification).filter(model_qualification.Qualification.applicant_id == applicant_id, model_qualification.Qualification.id == qualification_id).first()
    if not qualification:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"You are not authorized to modify the applicant qualification with id {qualification_id}")

    db.query(model_qualification.Qualification).filter(model_qualification.Qualification.id == qualification_id).delete()
    db.commit()

    return {"message": f"Successfully deleted applicant qualification with id: {qualification_id}"}