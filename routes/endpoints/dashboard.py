from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from config.database import get_db_connection
from models import user as model_user

from pydantic_schemas.user_type import UserTypes
from routes.endpoints.user import get_current_user
from services import job_position_service, user_service
from templates import templates


router = APIRouter()


@router.get("/", tags=["dashboard"], response_class=HTMLResponse)
@router.get("/dashboard/", tags=["dashboard"], response_class=HTMLResponse)
async def dashboard(request: Request, user_or_response: model_user.User | RedirectResponse = Depends(get_current_user),
                    db: Session = Depends(get_db_connection)):
    if isinstance(user_or_response, RedirectResponse):
        return user_or_response

    detailed_user = user_service.get_detailed_user(db, user_or_response)
    if UserTypes(user_or_response.user_type_id) == UserTypes.Employer:
        job_list = job_position_service.get_job_positions(db, detailed_user.id)
    else:
        job_list = job_position_service.get_applied_job_positions_by_applicant(db, detailed_user.id)

    data = {
        "request": request, "detailed_user": detailed_user, "user_type_id": user_or_response.user_type_id, "job_list": job_list
    }

    return templates.TemplateResponse("dashboard.html", data)
