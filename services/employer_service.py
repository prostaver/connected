from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import employer as model_employer
from pydantic_schemas import user as user_schema, employer as employer_schema

"""
    Retrieves the employer data.
"""
def get_employers(db: Session, employer_id: int = None):
    if employer_id:
        employer = db.query(model_employer.Employer).filter(model_employer.Employer.id == employer_id).first()
        if employer:
            return employer
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No employer found with id {employer_id}")
    employers = db.query(model_employer.Employer).all()
    return employers

"""
    Creates or updates the employer details for the user.
"""
def create_or_update_employer(db: Session, employer_input_data:employer_schema.CreateEmployer, user_id: int = None) -> model_employer.Employer:
    print("==================================================================================================================================")
    print(user_id)
    employer_data = get_employer_by_user_id(db, user_id, True)

    if employer_data: #Update existing employer
        employer_data.company_name = employer_input_data.company_name,
        employer_data.company_description = employer_input_data.company_description,
        employer_data.company_website = employer_input_data.company_website,
        employer_data.company_logo = employer_input_data.company_logo
    else: #Create new employer
        employer_data = model_employer.Employer(
            company_name = employer_input_data.company_name,
            company_description = employer_input_data.company_description,
            company_website = employer_input_data.company_website,
            company_logo = employer_input_data.company_logo,
            user_id = user_id
        )

    db.add(employer_data)
    db.commit()
    return employer_data

def get_employer_by_user_id(db: Session, user_id: int, accepts_none: bool = False) -> model_employer.Employer:
    employer_data = db.query(model_employer.Employer).filter(model_employer.Employer.user_id == user_id).first()
    if employer_data:
        return employer_data
    if not accepts_none:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No employer found with user id {user_id}")
    return None

def delete_employer(db: Session, employer_id: int):
    db.query(model_employer.Employer).filter(model_employer.Employer.id == employer_id).delete()
    db.commit()

    return {"message": f"Successfuly deleted employer detail with employer id: {employer_id}"}
