from datetime import datetime

from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from config.database import Base
from models.applicant import Applicant

class Qualification(Base):
    __tablename__ = "applicant_qualifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    details = Column(Text, nullable=False)
    acquirement_date = Column(DateTime, default=datetime.now)
    applicant_id = Column(Integer, ForeignKey("applicant_details.id"))

    applicant = relationship(Applicant)

    def __repr__(self):
        return f"<Qualification id = {self.id}, details = {self.details}, acquirement_date = {self.acquirement_date}, applicant_id = {self.applicant_id}>"
