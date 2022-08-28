from fastapi import Request


class LoginForm:
    def __init__(self, request: Request):
        form_data = await request.form()
        self.username = form_data.username
        self.password = form_data.password
