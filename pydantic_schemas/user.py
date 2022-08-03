from typing import Optional

from pydantic import BaseModel
from pydantic_schemas.gender import Gender
from pydantic_schemas.user_type import UserType

class BaseUser(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    address: str
    email: str
    contact_no: str
    user_type_id: int
    gender_id: int

class User(BaseUser):
    from models.user import User as ModelUser
    id: int

    user_type: UserType
    gender: Gender

    def __int__(self, user: ModelUser):
        self.id = user.id
        self.first_name = user.first_name
        self.middle_name = user.middle_name
        self.last_name = user.last_name
        self.address = user.address
        self.email = user.email
        self.contact_no = user.contact_no
        self.user_type_id = user.user_type_id
        self.gender_id = user.gender_id
        self.user_type = user.user_type
        self.gender = user.gender

    class Config:
        orm_mode = True

class CreateUser(BaseUser):
    password: Optional[str]

    from pydantic_schemas.employer import CreateEmployer
    employer: Optional[CreateEmployer]
