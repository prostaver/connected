from typing import Optional

from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm


class LoginForm(OAuth2PasswordRequestForm):
    def __init__(self, request: Request):
        # form_data = await request.form()
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_form_data(self):
        form_data = await self.request.form()
        self.username = form_data.get("username")
        self.password = form_data.get("password")
