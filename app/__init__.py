from fastapi import FastAPI

from .config import config_by_name, Config
from app import router
from .models import database


from .router.user.user import UserRouter
from .router.auth.auth import AuthRoutes
from .router.user.store import StoreRouter
from .router.offer.offer import OfferRouter,OfferTypeRouter
from .router.subscription.subscription import SubscriptionRouter,SubscriptionTypeRouter

def create_app():
    app = FastAPI()
    app.include_router(AuthRoutes().router)
    app.include_router(UserRouter().router)
    app.include_router(StoreRouter().router)
    app.include_router(OfferRouter().router)
    app.include_router(OfferTypeRouter().router)

    app.include_router(SubscriptionRouter().router)
    app.include_router(SubscriptionTypeRouter().router)
    
    return app
