from sqlalchemy import Column, String, Integer, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from config.database import Base
from models.employer import Employer

class JobPosition(Base):
    __tablename__ = "job_positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    salary = Column(Numeric(precision=11, scale=4))
    employer_id = Column(Integer, ForeignKey("employer_details.id"))

    employer = relationship(Employer)

    def __repr__(self):
        return f"<JobPosition id = {self.id}, title = {self.title}, description = {self.description}, salary = {self.salary}, employer_id = {self.employer_id}"
