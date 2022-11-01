from typing import Optional

from fastapi import Request, UploadFile

from pydantic_schemas.user import CreateUser


class UserForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.id: Optional[int] = None
        self.first_name: Optional[str] = None
        self.middle_name: Optional[str] = None
        self.last_name: Optional[str] = None
        self.address: Optional[str] = None
        self.email: Optional[str] = None
        self.contact_no: Optional[str] = None
        self.password: Optional[str] = None
        self.user_type_id: Optional[int] = None
        self.gender_id: Optional[int] = None
        self.user_img: Optional[UploadFile] = None

    async def load_form_data(self):
        form_data = await self.request.form()

        self.first_name = form_data.get("first_name")
        self.middle_name = form_data.get("middle_name")
        self.last_name = form_data.get("last_name")
        self.address = form_data.get("address")
        self.email = form_data.get("email")
        self.contact_no = form_data.get("contact_no")
        self.user_type_id = form_data.get("user_type_id")
        self.gender_id = form_data.get("gender_id")
        self.password = form_data.get("password")
        self.user_img = form_data.get("user_img")

    def form_to_schema(self) -> CreateUser:
        user_data = CreateUser(
            first_name=self.first_name,
            middle_name=self.middle_name,
            last_name=self.last_name,
            address=self.address,
            email=self.email,
            contact_no=self.contact_no,
            user_type_id=self.user_type_id,
            gender_id=self.gender_id,
            password=self.password,
            user_upload_img=self.user_img
        )

        return user_data
