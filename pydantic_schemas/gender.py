from pydantic import BaseModel

class Gender(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True