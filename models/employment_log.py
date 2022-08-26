from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from config.database import Base
from models.applicant import Applicant
from models.job_position import JobPosition


class EmploymentLog(Base):
    __tablename__ = "employment_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=True)
    position = Column(String(255), nullable=False)
    tenure = Column(String(255), nullable=False)
    is_current = Column(Boolean, default=True)
    applicant_id = Column(Integer, ForeignKey("applicant_details.id"))
    job_position_id = Column(Integer, ForeignKey("job_positions.id"), nullable=True)

    applicant = relationship(Applicant)
    job_position = relationship(JobPosition)

    def __repr__(self):
        return (f"<EmploymentLog id = {self.id}, company_name = {self.company_name}, position = {self.position}, "
                f"tenure = {self.tenure}, is_current = {self.is_current}, applicant_id = {self.applicant_id}, "
                f"employer_id = {self.job_position_id}>")
