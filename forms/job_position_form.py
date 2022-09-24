from decimal import Decimal
from typing import Optional

from fastapi import Request

from pydantic_schemas.job_position import CreateJobPosition


class JobPositionForm:
    def __init__(self, request: Request):
        self.request = request
        self.title: Optional[str] = None
        self.description: Optional[str] = None
        self.salary: Optional[Decimal] = None
        self.employer_id: Optional[int] = None

    async def load_form_data(self):
        form_data = await self.request.form()
        self.title = form_data.get("title")
        self.description = form_data.get("description")
        self.salary = form_data.get("salary")
        self.employer_id = form_data.get("form_employer_id")

    def form_to_schema(self) -> CreateJobPosition:
        job_position_data = CreateJobPosition(
            title=self.title,
            description=self.description,
            salary=self.salary,
            employer_id=self.employer_id,
        )

        return job_position_data
