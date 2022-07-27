from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from config.database import Base
from models.applicant import Applicant
from models.employer import Employer

class EmploymentLog(Base):
    __tablename__ = "employment_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=True)
    position = Column(String(255), nullable=False)
    tenure = Column(String(255), nullable=False)
    is_current = Column(Boolean, default=True)
    applicant_id = Column(Integer, ForeignKey("applicant_details.id"))
    employer_id = Column(Integer, ForeignKey("employer_details.id"), nullable=True)

    applicant = relationship(Applicant)
    employer = relationship(Employer)

    def __repr__(self):
        return (f"<EmploymentLog id = {self.id}, company_name = {self.company_name}, position = {self.position}, tenure = {self.tenure}, " +
                f"is_current = {self.is_current}, applicant_id = {self.applicant_id}, employer_id = {self.employer_id}>")
