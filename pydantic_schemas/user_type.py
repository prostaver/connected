from enum import Enum

from pydantic import BaseModel


class UserTypes(Enum):
    Employer = 1
    Applicant = 2


class UserType(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
