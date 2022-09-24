from typing import List, Optional

from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic_schemas import user as user_schema
from sqlalchemy.orm import Session

from config.database import get_db_connection
from forms.login_form import LoginForm
from forms.user_form import UserForm
from pydantic_schemas.user_type import UserTypes
from routes.endpoints.login import login_token, oauth2_scheme_cookie
from services import applicant_service, gender_service, login_service, user_service, user_type_service
from templates import templates

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


@router.get("/signup/", response_class=HTMLResponse)
async def get_create_user_form(request: Request, db: Session = Depends(get_db_connection)):
    genders = gender_service.get_genders(db)
    user_types = user_type_service.get_user_types(db)
    data = {
        "request": request,
        "genders": genders,
        "user_types": user_types
    }

    return templates.TemplateResponse("signup.html", data)


@router.post('/signup/', response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def post_user_form(request: Request, db: Session = Depends(get_db_connection)):
    user_form = UserForm(request)
    await user_form.load_form_data()
    user_data = user_form.form_to_schema()
    saved_user = await create_user(user_data, db)

    # response = RedirectResponse(request.url_for("get_employer_form"), status.HTTP_303_SEE_OTHER)
    if UserTypes(user_data.user_type_id) == UserTypes.Employer:
        response = templates.TemplateResponse("employer_form.html", {"request": request, "user_id": saved_user.id})
    else:
        applicant_service.create_applicant(db, saved_user.id)
        response = RedirectResponse(request.url_for("dashboard"), status.HTTP_303_SEE_OTHER)

    login_form = object.__new__(LoginForm)
    login_form.new(username=user_form.email, password=user_form.password)
    login_token(response, login_form, db)
    return response
