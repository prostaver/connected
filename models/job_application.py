from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from config.database import Base
from models.applicant import Applicant
from models.job_position import JobPosition


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    applicant_id = Column(Integer, ForeignKey("applicant_details.id"))
    job_position_id = Column(Integer, ForeignKey("job_positions.id"))
    status = Column(Integer, nullable=False)

    applicant = relationship(Applicant)
    job_position = relationship(JobPosition)

    def __repr__(self):
        return f"<JobApplication id = {self.id}, first_name = {self.applicant_id}," \
               f" middle_name = {self.job_position_id}>"
