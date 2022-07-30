from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base
from models.user_type import UserType
from models.gender import Gender

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    middle_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    contact_no = Column(String(255), nullable=True)
    password = Column(Text, nullable=False)
    user_type_id = Column(Integer, ForeignKey("user_types.id"))
    gender_id = Column(Integer, ForeignKey("genders.id"))

    user_type = relationship(UserType)
    gender = relationship(Gender)

    def __repr__(self):
        return f"<User id = {self.id}, first_name = {self.first_name}, middle_name = {self.middle_name}, last_name = {self.last_name}, last_name = {self.email}>"
