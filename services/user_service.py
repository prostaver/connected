from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import getDbConection
from pydantic_schemas import user as user_schema
from models import user as model_user 

def getUsers(user_id:int = None, db: Session=Depends(getDbConection)):
    if(user_id):
        user = db.query(model_user.User).filter(model_user.User.id==user_id).first()
        if(user):
            return user
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"No user with id {user_id} was found")
    return db.query(user_id.User).all()

def createOrUpdateUser(user_schema:user_schema.CreateUser, user_id:int = None, db: Session=Depends(getDbConection)):
    user_data = None
    if(user_id):
        user_data = getUsers(user_id=user_id, db=db)
        user_data.first_name = user_schema.first_name
        user_data.middle_name = user_schema.middle_name
        user_data.last_name = user_schema.last_name
        user_data.address = user_schema.address
        user_data.email = user_schema.email
        user_data.contact_no = user_schema.contact_no
        user_data.password = user_schema.password
        user_data.user_type_id = user_schema.user_type_id
        user_data.gender_id = user_schema.gender_id
    else:
        user_data = user_schema.Student(
            first_name = user_schema.first_name,
            middle_name = user_schema.middle_name,
            last_name = user_schema.last_name,
            address = user_schema.address,
            email = user_schema.email,
            contact_no = user_schema.contact_no,
            password = user_schema.password,
            user_type_id = user_schema.user_type_id,
            is_active = user_schema.is_active
        )

    db.add(user_data)
    db.commit()

    return user_data