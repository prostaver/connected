from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .user import get_current_user
from config.database import get_db_connection
from forms.job_position_form import JobPositionForm
from models import user as model_user
from pydantic_schemas import job_position as job_position_schema, user as user_schema
from services import employer_service, job_position_service, user_service
from templates import templates

router = APIRouter(
    prefix="/job_positions",
    tags=["job_positions"]
)


@router.get("/", response_model=list[job_position_schema.JobPosition], status_code=status.HTTP_200_OK)
async def get_job_positions(db: Session = Depends(get_db_connection)):
    job_positions = job_position_service.get_job_positions(db)
    return job_positions


@router.get("/by_current_user", response_model=list[job_position_schema.JobPosition], status_code=status.HTTP_200_OK)
async def get_job_positions_by_current_user(db: Session = Depends(get_db_connection),
                                            user: user_schema.User = Depends(get_current_user)):
    employer = employer_service.get_employer_by_user_id(db, user.id)
    job_positions = job_position_service.get_job_positions(db, employer.id)
    return job_positions


@router.get("/{job_position_id}", response_model=job_position_schema.JobPosition, status_code=status.HTTP_200_OK)
async def get_job_position(job_position_id: int, employer_id: int = None, db: Session = Depends(get_db_connection)):
    job_position = job_position_service.get_job_positions(db, employer_id, job_position_id)
    return job_position


@router.post("/", response_model=job_position_schema.JobPosition, status_code=status.HTTP_201_CREATED)
async def create_job_position(job_position_input: job_position_schema.CreateJobPosition,
                              db: Session = Depends(get_db_connection)):
    job_position = job_position_service.create_job_position(db, job_position_input)
    return job_position


@router.delete("/{job_position_id}", status_code=status.HTTP_200_OK)
async def delete_job_position(job_position_id: int, employer_id: int, db: Session = Depends(get_db_connection)):
    return job_position_service.delete_job_position(db, job_position_id, employer_id)


@router.get("/form/create", response_class=HTMLResponse)
async def form_create_job_position(request: Request,
                                   user_or_response: RedirectResponse | model_user.User = Depends(get_current_user),
                                   db: Session = Depends(get_db_connection)):
    if isinstance(user_or_response, RedirectResponse):
        return user_or_response

    detailed_user = user_service.get_detailed_user(db, user_or_response)
    data = {
        "request": request, "detailed_user": detailed_user, "user_type_id": user_or_response.user_type_id
    }

    return templates.TemplateResponse("job_position_form.html", data)


@router.post("/form/create", response_class=HTMLResponse, status_code=status.HTTP_201_CREATED)
async def form_post_job_position(request: Request, db: Session = Depends(get_db_connection)):
    job_position_form = JobPositionForm(request)
    await job_position_form.load_form_data()
    job_position_data = job_position_form.form_to_schema()
    await create_job_position(job_position_data, db)

    return RedirectResponse(request.url_for("dashboard"), status.HTTP_303_SEE_OTHER)


@router.get("/find_jobs/", response_class=HTMLResponse)
async def find_job_page(request: Request,
                        user_or_response: RedirectResponse | model_user.User = Depends(get_current_user),
                        db: Session = Depends(get_db_connection)):
    if isinstance(user_or_response, RedirectResponse):
        return user_or_response

    detailed_user = user_service.get_detailed_user(db, user_or_response)
    jobs = await get_job_positions(db)
    data = {
        "request": request, "detailed_user": detailed_user, "user_type_id": user_or_response.user_type_id, "jobs": jobs
    }

    return templates.TemplateResponse("jobs.html", data)


@router.get("/{job_id}/details/", response_class=HTMLResponse)
async def get_job_details(job_id: int, request: Request,
                          user_or_response: RedirectResponse | model_user.User = Depends(get_current_user),
                          db: Session = Depends(get_db_connection)):
    if isinstance(user_or_response, RedirectResponse):
        return user_or_response

    detailed_user = user_service.get_detailed_user(db, user_or_response)
    job = await get_job_position(job_id, None, db)
    data = {
        "request": request, "detailed_user": detailed_user, "user_type_id": user_or_response.user_type_id, "job": job
    }

    return templates.TemplateResponse("job_detail.html", data)
