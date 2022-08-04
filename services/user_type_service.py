from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user_type import UserType

def get_user_types(db: Session, user_type_id: int = None):
    if user_type_id:
        user_type = db.query(UserType).filter(UserType.id == user_type_id).first()
        if not user_type:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"No user type found with user type id: {user_type_id}")
        return user_type
    
    return db.query(UserType).all()
