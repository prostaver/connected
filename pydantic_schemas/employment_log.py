from typing import Optional

from pydantic import BaseModel

from pydantic_schemas.applicant import Applicant
from pydantic_schemas.job_position import JobPosition


class BaseEmploymentLog(BaseModel):
    company_name: str
    position: str
    tenure: str
    is_current: bool


class CreateEmploymentLog(BaseEmploymentLog):
    applicant_id: int
    job_position_id: Optional[int]


class EmploymentLog(BaseEmploymentLog):
    id: int

    applicant: Applicant
    job_position: Optional[JobPosition]

    class Config:
        orm_mode = True
