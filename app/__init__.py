from fastapi import FastAPI



from .config import config_by_name, Config
from app import router
from .models import database


from .router.user.user import UserRouter
from .router.auth.auth import AuthRoutes
from .router.user.store import StoreRouter
from .router.offer.offer import OfferRouter,OfferTypeRouter
from .router.subscription.subscription import SubscriptionRouter,SubscriptionTypeRouter
from .router.transaction.transaction import TransactionRouter
from .router.stats.stats import StatsRouter
from .router.search.search import SearchRouter
from .router.storage.storage import StorageRouter

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
