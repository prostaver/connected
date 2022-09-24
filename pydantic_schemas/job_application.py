from enum import Enum

from pydantic import BaseModel

from pydantic_schemas.applicant import Applicant
from pydantic_schemas.job_position import JobPosition


class JobApplicationStatus(Enum):
    Applied = 1
    Accepted = 2
    Rejected = 3


class BaseJobApplication(BaseModel):
    applicant_id: int
    job_position_id: int
    status: int


class CreateJobApplication(BaseJobApplication):
    pass


class JobApplication(BaseJobApplication):
    id: int

    applicant: Applicant
    job_position: JobPosition

    class Config:
        orm_mode = True
