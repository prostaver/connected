from fastapi import APIRouter
from routes.endpoints import (user, login)

router = APIRouter()

router.include_router(user.router)
router.include_router(login.router)