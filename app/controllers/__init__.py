from fastapi import APIRouter
from app.controllers.users import router as users_router
from app.controllers.users.create_user import router as create_user_router
from app.controllers.users.delete_user import router as delete_user_router
from app.controllers.users.delete_all_users import router as delete_all_users_router
from app.controllers.users.get_all_users import router as get_all_users_router
from app.controllers.users.get_user import router as get_user_router
from app.controllers.users.login import router as login_router
from app.controllers.users.update_email import router as update_email_router
from app.controllers.users.update_password import router as update_password_router
from app.controllers.users.update_username import router as update_username_router

router = APIRouter()
router.include_router(users_router)
router.include_router(create_user_router)
router.include_router(delete_user_router)
router.include_router(delete_all_users_router)
router.include_router(get_user_router)
router.include_router(get_all_users_router)
router.include_router(login_router)
router.include_router(update_email_router)
router.include_router(update_password_router)
router.include_router(update_username_router)