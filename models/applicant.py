from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base
from models.user import User


class Applicant(Base):
    __tablename__ = "applicant_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship(User)

    def __repr__(self):
        return f"<Applicant id = {self.id}, user_id = {self.user_id}"
