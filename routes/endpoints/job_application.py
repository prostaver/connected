from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from config.database import get_db_connection
from forms.job_application_form import JobApplicationForm
from pydantic_schemas import job_application as job_application_schema
from pydantic_schemas import user as user_schema
from routes.endpoints.user import get_current_user
from services import job_application_service


router = APIRouter(
    prefix="/job_applications",
    tags=["job_applications"]
)


@router.post("/", response_model=job_application_schema.JobApplication, status_code=status.HTTP_201_CREATED)
async def create_job_application(ja_input: job_application_schema.CreateJobApplication,
                                 db: Session = Depends(get_db_connection)):

    return job_application_service.create_job_application(db, ja_input)


@router.get("/", response_model=list[job_application_schema.JobApplication], status_code=status.HTTP_200_OK)
async def get_job_applications(db: Session = Depends(get_db_connection)):
    return job_application_service.get_job_applications(db)


@router.get("/{ja_id}", response_model=job_application_schema.JobApplication, status_code=status.HTTP_200_OK)
async def get_job_application(ja_id: int, db: Session = Depends(get_db_connection)):
    return job_application_service.get_job_application(db, ja_id)


@router.post("/{ja_id}", response_model=job_application_schema.JobApplication, status_code=status.HTTP_200_OK)
async def update_job_application(ja_input: job_application_schema.CreateJobApplication,
                                 ja_id: int, db: Session = Depends(get_db_connection)):
    return job_application_service.update_job_application(db, ja_input, ja_id)


@router.post("/{ja_id}", status_code=status.HTTP_200_OK)
async def delete_job_application(ja_id: int, db: Session = Depends(get_db_connection)):
    return job_application_service.delete_job_application(db, ja_id)


@router.post("/form/", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def post_job_application_form(request: Request,
                                    user_or_response: RedirectResponse | user_schema.User = Depends(get_current_user),
                                    db: Session = Depends(get_db_connection)):
    if isinstance(user_or_response, RedirectResponse):
        return user_or_response

    ja_form = JobApplicationForm(request)
    await ja_form.load_form_data()
    ja_data = ja_form.form_to_schema()
    await create_job_application(ja_data, db)

    return RedirectResponse(request.url_for("dashboard"), status.HTTP_303_SEE_OTHER)
