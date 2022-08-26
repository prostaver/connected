from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from config.database import Base
from models.user import User


class Employer(Base):
    __tablename__ = "employer_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    company_description = Column(Text, nullable=True)
    company_website = Column(String(255), nullable=True)
    company_logo = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship(User)

    def __repr__(self):
        return (
                    f"<Employer id = {self.id}, company_name = {self.company_name}, company_description = {self.company_description}, " +
                    f"company_website = {self.company_website}, complany_logo = {self.company_logo}, user_id = {self.user_id}")
