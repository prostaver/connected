from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.database import get_db_connection
from services import login_service

router = APIRouter(
    prefix = "/login",
    tags={"login"}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_connection)):
    return login_service.create_auth_token(db, form_data.username, form_data.password)
