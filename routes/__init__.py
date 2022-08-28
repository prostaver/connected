from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from routes.endpoints import (applicant, employer, employment_log, gender, job_position, login, qualification, user,
                              user_type)

router = APIRouter()

router.include_router(login.router)
router.include_router(user_type.router)
router.include_router(gender.router)
router.include_router(user.router)
router.include_router(employer.router)
router.include_router(job_position.router)
router.include_router(applicant.router)
router.include_router(qualification.router)
router.include_router(employment_log.router)


# TODO Temporary location for the dashboard route.
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    from templates import templates
    return templates.TemplateResponse("dashboard.html", {"request": request})
