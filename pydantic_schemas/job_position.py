from decimal import Decimal

from pydantic import BaseModel
from pydantic_schemas.employer import Employer


class BaseJobPosition(BaseModel):
    title: str
    description: str
    salary: Decimal
    employer_id: int


class CreateJobPosition(BaseJobPosition):
    pass


class JobPosition(BaseJobPosition):
    id: int

    employer: Employer

    class Config:
        orm_mode = True
