from pydantic import BaseModel


class BaseApplicant(BaseModel):
    user_id: int


class CreateApplicant(BaseApplicant):
    pass


class Applicant(BaseApplicant):
    id: int

    from .user import User
    user: User

    class Config:
        orm_mode = True
