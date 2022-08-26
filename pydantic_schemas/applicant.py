from pydantic import BaseModel


class BaseApplicant(BaseModel):
    user_id: int # TODO Move to Applicant if additional fields are added to applicant details model, but if not,
    # TODO remove BaseApplicant and CreateApplicant and leave only Applicant class in this file.


class CreateApplicant(BaseApplicant):
    pass


class Applicant(BaseApplicant):
    id: int

    from .user import User
    user: User

    class Config:
        orm_mode = True
