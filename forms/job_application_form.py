from typing import Optional

from fastapi import Request

from pydantic_schemas.job_application import CreateJobApplication


class JobApplicationForm:
    def __init__(self, request: Request):
        self.request = request
        self.applicant_id: Optional[int] = None
        self.job_position_id: Optional[int] = None
        self.status: Optional[int] = None

    async def load_form_data(self):
        form_data = await self.request.form()
        self.applicant_id = form_data.get("form_applicant_id")
        self.job_position_id = form_data.get("form_job_position_id")
        self.status = 1

    def form_to_schema(self) -> CreateJobApplication:
        job_application_data = CreateJobApplication(
            applicant_id=self.applicant_id,
            job_position_id=self.job_position_id,
            status=self.status,
        )

        return job_application_data
