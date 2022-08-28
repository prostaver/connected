from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.database import get_db_connection
from handlers.auth_bearer_with_cookie_handler import OAuth2PasswordBearerWithCookie
from services import login_service
from templates import templates

router = APIRouter(
    prefix="/login",
    tags=["login"]
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
oauth2_scheme_cookie = OAuth2PasswordBearerWithCookie(tokenUrl="login")


@router.post("/token")
async def login_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_connection)):
    # form_data = await request.form()
    access_token = login_service.create_auth_token(db, form_data.username, form_data.password)
    request.set_cookie(key="access_token",value=f"Bearer {access_token}", httponly=True)
    return login_service.create_auth_token(db, form_data.username, form_data.password)


@router.post("/")
async def login(request: Request, db: Session = Depends(get_db_connection)):
    form_data = await request.form()
    return login_service.create_auth_token(db, form_data.username, form_data.password)


@router.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
