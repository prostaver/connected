from fastapi import APIRouter
from routes.endpoints import user

router = APIRouter()

#router.include_router(student.router)
#router.include_router(dtr.router)
router.include_router(user.router)
