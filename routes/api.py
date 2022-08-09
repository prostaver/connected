from fastapi import APIRouter
from routes.endpoints import (applicant, employer, employment_log, gender, job_position, login, user, user_type)

router = APIRouter()

router.include_router(login.router)
router.include_router(user_type.router)
router.include_router(gender.router)
router.include_router(user.router)
router.include_router(employer.router)
router.include_router(job_position.router)
router.include_router(applicant.router)
#router.include_router(employment_log.router)