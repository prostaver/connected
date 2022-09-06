from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from config.database import get_db_connection
from models import user as model_user

from routes.endpoints.user import get_current_user
from services import user_service
from templates import templates


router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, user_or_response: model_user.User | RedirectResponse = Depends(get_current_user),
                    db: Session = Depends(get_db_connection)):
    if isinstance(user_or_response, RedirectResponse):
        return user_or_response

    detailed_user = user_service.get_detailed_user(db, user_or_response)
    data = {
        "user": detailed_user, "user_type_id": user_or_response.user_type_id
    }

    return templates.TemplateResponse("dashboard.html", {"request": request, "data": data})
