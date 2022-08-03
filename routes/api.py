from fastapi import APIRouter
from routes.endpoints import (user, login, employer)

router = APIRouter()

router.include_router(login.router)
router.include_router(user.router)
router.include_router(employer.router)