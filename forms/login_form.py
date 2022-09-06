from typing import Optional

from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    def new(self, username: str, password: str):
        self.username = username
        self.password = password

    async def load_form_data(self):
        form_data = await self.request.form()
        self.username = form_data.get("username")
        self.password = form_data.get("password")
