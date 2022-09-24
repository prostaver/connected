from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from config.database import get_db_connection
from forms.login_form import LoginForm
from handlers.auth_bearer_with_cookie_handler import OAuth2PasswordBearerWithCookie
from services import login_service
from templates import templates

router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme_cookie = OAuth2PasswordBearerWithCookie(tokenUrl="login/token")


@router.post("/login/token", tags=["login"])
def login_token(response: Response, form_data: LoginForm = Depends(),
                db: Session = Depends(get_db_connection)):
    return login_service.create_auth_token(db, form_data.username, form_data.password, response)


@router.post("/login/", tags=["login"], response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db_connection)):
    form = LoginForm(request)
    try:
        response = RedirectResponse(request.url_for("dashboard"), status.HTTP_303_SEE_OTHER)
        await form.load_form_data()
        login_token(response=response, form_data=form, db=db)
        return response
    except HTTPException as e:
        form.__dict__.update(errors=e.detail)
        return templates.TemplateResponse("login.html", form.__dict__)


@router.get("/login/", tags=["login"], response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/logout/", tags=["logout"], response_class=HTMLResponse)
async def logout(request: Request):
    response = RedirectResponse(request.url_for("login"), status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response
