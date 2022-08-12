from datetime import date

from pydantic import BaseModel

from pydantic_schemas.applicant import Applicant

class BaseQualification(BaseModel):
    details: str
    acquirement_date: date
    applicant_id: int

class CreateQualification(BaseQualification):
    pass

class Qualification(BaseQualification):
    id: int

    applicant: Applicant

    class Config:
        orm_mode = True
