from fastapi import APIRouter
from app.controllers.users.get_user import router as get_user_router
router = APIRouter()
router.include_router(get_user_router)