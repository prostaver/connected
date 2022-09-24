from typing import List

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from config.database import get_db_connection
from forms.employer_form import EmployerForm
from models import user as model_user
from pydantic_schemas import employer as employer_schema
from routes.endpoints.user import get_current_user
from services import employer_service
from templates import templates

router = APIRouter(
    prefix="/employers",
    tags=["employers"]
    # dependencies=Depends(token)
)


@router.get("/", response_model=List[employer_schema.Employer], status_code=status.HTTP_200_OK)
async def get_employers(db: Session = Depends(get_db_connection)):
    return employer_service.get_employers(db)


@router.get("/{employer_id}", response_model=employer_schema.Employer, status_code=status.HTTP_200_OK)
async def get_employer(employer_id: int, db: Session = Depends(get_db_connection)):
    return employer_service.get_employers(db, employer_id)


@router.delete("/{employer_id}", status_code=status.HTTP_200_OK)
async def delete_employer(employer_id: int, db: Session = Depends(get_db_connection)):
    return employer_service.delete_employer(db, employer_id)


@router.post("/", response_model=employer_schema.Employer, status_code=status.HTTP_201_CREATED)
async def create_or_update_employer(employer_input_data: employer_schema.CreateEmployer,
                                    db: Session = Depends(get_db_connection)):
    return employer_service.create_or_update_employer(db, employer_input_data)


@router.get("/form/create", response_class=HTMLResponse)
async def get_employer_form(request: Request,
                            user_or_response: model_user.User | RedirectResponse = Depends(get_current_user)):
    if isinstance(user_or_response, RedirectResponse):
        return user_or_response

    data = {
        "request": request, "user_id": user_or_response.id
    }

    return templates.TemplateResponse("employer_form.html", data)


@router.post("/form/create")
async def post_employer_form(request: Request, db: Session = Depends(get_db_connection)):
    employer_form = EmployerForm(request)
    await employer_form.load_form_data()
    employer_data = employer_form.form_to_schema()
    await create_or_update_employer(employer_data, db)

    return RedirectResponse(request.url_for("dashboard"), status.HTTP_303_SEE_OTHER)
