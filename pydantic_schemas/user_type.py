from pydantic import BaseModel

class UserType(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True