from typing import List, Optional

from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import RedirectResponse
from pydantic_schemas import user as user_schema
from sqlalchemy.orm import Session

# from routes.endpoints.login import oauth2_scheme
from routes.endpoints.login import oauth2_scheme_cookie
from config.database import get_db_connection
from services import user_service, login_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=List[user_schema.User], status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db_connection)):
    users = user_service.get_users(db=db)
    return users


@router.get("/{user_id}", response_model=user_schema.User, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: Session = Depends(get_db_connection)):
    user = user_service.get_users(db=db, user_id=user_id)
    return user


@router.post('/', response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
async def create_user(user_input: user_schema.CreateUser, db: Session = Depends(get_db_connection)):
    new_user = user_service.create_or_update_user(db=db, user_input=user_input)
    return new_user


@router.post('/{user_id}', response_model=user_schema.User, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user_input: user_schema.CreateUser, db: Session = Depends(get_db_connection)):
    updated_user = user_service.create_or_update_user(db=db, user_id=user_id, user_input=user_input)
    return updated_user


@router.get("/current/", response_model=user_schema.User, status_code=status.HTTP_200_OK)
async def get_current_user(request: Request, token: Optional[str] = Depends(oauth2_scheme_cookie),
                           db: Session = Depends(get_db_connection)):
    # if isinstance(token, RedirectResponse):
    #     return token

    if token is not None:
        payload = login_service.decode_token(token)

        if payload is not None:
            user = user_service.get_user_by_email(db=db, email=payload.get("user_email"))
            # detailed_user = user_service.get_detailed_user(db, user)

            return user
    return RedirectResponse(request.url_for("login"), status.HTTP_303_SEE_OTHER)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db_connection)):
    return user_service.delete_user(db, user_id)
