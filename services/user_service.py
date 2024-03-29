from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .hash_func import hash_password
from models import user as model_user
from pydantic_schemas import user as user_schema, user_type as user_type_schema
from services import employer_service, applicant_service

"""
    Retrieves the user data
"""


def get_users(db: Session, user_id: int = None):
    if user_id:
        user = db.query(model_user.User).filter(model_user.User.id == user_id).first()
        if user:
            return user
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"No user with id {user_id} was found")
    return db.query(model_user.User).all()


def create_or_update_user(db: Session, user_input: user_schema.CreateUser, user_id: int = None):
    hashed_password = None
    unhashed_password = user_input.password

    if unhashed_password:
        hashed_password = hash_password(unhashed_password)

    if user_id:
        user_data = get_users(user_id=user_id, db=db)
        user_data.first_name = user_input.first_name
        user_data.middle_name = user_input.middle_name
        user_data.last_name = user_input.last_name
        user_data.address = user_input.address
        user_data.email = user_input.email
        user_data.contact_no = user_input.contact_no
        user_data.user_type_id = user_input.user_type_id
        user_data.gender_id = user_input.gender_id
        if hashed_password:
            user_data.password = hashed_password
        if user_input.user_upload_img.filename:
            user_data.user_img = user_input.user_upload_img.filename
    else:
        user_data = model_user.User(
            first_name=user_input.first_name,
            middle_name=user_input.middle_name,
            last_name=user_input.last_name,
            address=user_input.address,
            email=user_input.email,
            contact_no=user_input.contact_no,
            user_type_id=user_input.user_type_id,
            gender_id=user_input.gender_id
        )
        if hashed_password:
            user_data.password = hashed_password
        if user_input.user_upload_img.filename:
            user_data.user_img = user_input.user_upload_img.filename

    db.add(user_data)
    db.commit()

    # employer_input_data = user_input.employer
    # if user_type_schema.UserTypes(user_data.user_type_id) == user_type_schema.UserTypes.Employer:
    #     employer_service.create_or_update_employer(db=db, employer_input_data=employer_input_data, user_id=user_data.id)
    # elif user_type_schema.UserTypes(user_data.user_type_id) == user_type_schema.UserTypes.Applicant:
    #     applicant_service.create_applicant(db, user_data.id)

    return user_data


def get_user_by_email(db: Session, email: str):
    user = db.query(model_user.User).filter(model_user.User.email == email).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Incorrect username or password", {"WWW-Authenticate": "Bearer"})
    return user


def delete_user(db: Session, user_id: int):
    user = get_users(db, user_id)
    if user_type_schema.UserTypes(user.user_type_id) == user_type_schema.UserTypes.Employer:
        employer = employer_service.get_employer_by_user_id(db, user_id, True)
        if employer:
            employer_service.delete_employer(db, employer.id)
    if user_type_schema.UserTypes(user.user_type_id) == user_type_schema.UserTypes.Applicant:
        applicant = applicant_service.get_applicant_by_user_id(db, user_id)
        if applicant:
            applicant_service.delete_applicant(db, applicant.id)

    db.query(model_user.User).filter(model_user.User.id == user_id).delete()
    db.commit()

    return {"message": f"Successfully deleted user with id: {user_id}"}


def get_detailed_user(db: Session, user: model_user.User):
    if user_type_schema.UserTypes(user.user_type_id) == user_type_schema.UserTypes.Employer:
        detailed_user = employer_service.get_employer_by_user_id(db, user.id)
    else:
        detailed_user = applicant_service.get_applicant_by_user_id(db, user.id)
    return detailed_user
