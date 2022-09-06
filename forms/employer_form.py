from typing import Optional

from fastapi import Request

from pydantic_schemas.employer import CreateEmployer


class EmployerForm:
    def __init__(self, request: Request):
        self.request = request
        self.company_name: Optional[str] = None
        self.company_description: Optional[str] = None
        self.company_website: Optional[str] = None
        self.company_logo: Optional[str] = None
        self.user_id: Optional[int] = None

    async def load_form_data(self):
        form_data = await self.request.form()
        self.company_name = form_data.get("company_name")
        self.company_description = form_data.get("company_description")
        self.company_website = form_data.get("company_website")
        self.company_logo = form_data.get("company_logo")
        self.user_id = form_data.get("user_id")

    def form_to_schema(self) -> CreateEmployer:
        employer_data = CreateEmployer(
            company_name=self.company_name,
            company_description=self.company_description,
            company_website=self.company_website,
            company_logo=self.company_logo,
            user_id=self.user_id
        )

        return employer_data
