from fastapi import FastAPI

from .config import config_by_name, Config
from app import router
from .models import database


from .router.user.user import UserRouter
from .router.auth.auth import AuthRoutes

def create_app():
    app = FastAPI()
    app.include_router(AuthRoutes().router)
    app.include_router(UserRouter().router)
    return app
