from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from config.database import Base

class Gender(Base):
    __tablename__ = "genders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(6), nullable=False)

    def __repr__(self):
        return f"<Gender id = {self.id}, name = {self.name}>"
