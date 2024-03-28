from fastapi import FastAPI



from .config import config_by_name, Config
from app import router
from .models import database


from .router.user import UserRouter
from .router.auth import AuthRoutes
from .router.store import StoreRouter
from .router.offer import OfferRouter,OfferTypeRouter
from .router.subscription import SubscriptionRouter,SubscriptionTypeRouter
from .router.transaction import TransactionRouter
from .router.stats import StatsRouter
from .router.search import SearchRouter
from .router.storage import StorageRouter

def create_app():
    app = FastAPI()
    app.include_router(AuthRoutes().router)
    app.include_router(UserRouter().router)
    app.include_router(StoreRouter().router)
    app.include_router(OfferRouter().router)
    app.include_router(OfferTypeRouter().router)

    app.include_router(SubscriptionRouter().router)
    app.include_router(SubscriptionTypeRouter().router)

    app.include_router(TransactionRouter().router)

    app.include_router(StatsRouter().router)

    app.include_router(SearchRouter().router)
    
    app.include_router(StorageRouter().router)
    return app
