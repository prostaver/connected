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

class CreateUser(BaseUser):
    password: str

class User(BaseModel):
    id: int

    user_type_id: UserType
    gender: Gender

    class Config:
        orm_mode = True
