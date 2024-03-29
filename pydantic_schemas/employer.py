from typing import Optional
from pydantic import BaseModel


class BaseEmployer(BaseModel):
    company_name: str
    company_description: str
    company_website: Optional[str]
    company_logo: Optional[str]
    user_id: int


class CreateEmployer(BaseEmployer):
    pass


class Employer(BaseEmployer):
    id: int

    from pydantic_schemas.user import User
    user: User
    
    class Config:
        orm_mode = True
