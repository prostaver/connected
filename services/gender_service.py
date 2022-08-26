from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.gender import Gender


def get_genders(db: Session, gender_id: int = None):
    if gender_id:
        gender = db.query(Gender).filter(Gender.id == gender_id).first()
        if not gender:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"No gender found with id: {gender_id}")
        return gender
    
    return db.query(Gender).all()
