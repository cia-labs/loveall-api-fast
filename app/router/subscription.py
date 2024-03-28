from fastapi import APIRouter
from app.services.offer.offer import OfferService,OfferTypeService
from app.services.subscription.subscription import SubscriptionService,SubscriptionTypeService
from fastapi import FastAPI, Body, Depends
from app.services.auth.auth_bearer import get_current_user

class SubscriptionTypeRouter:
    """
    Router for offer type
    """

    def __init__(self):
        """
        Constructor for subscriptiontype router
        """
        self.subscriptionTypeRouter = SubscriptionTypeService()
        self.router = APIRouter(prefix='/subscriptionType',tags=['subscriptionType'])
        self.router.add_api_route(path='/{subscription_type_id:path}', methods=['GET'],dependencies=[Depends(get_current_user)],
                                  endpoint=self.subscriptionTypeRouter.fetch_subscription_type)
        
        self.router.add_api_route(path='/create', methods=['POST'],dependencies=[Depends(get_current_user)],
                                  endpoint=self.subscriptionTypeRouter.create_subscription_type)
        self.router.add_api_route(path='/update/{subscription_type_id:path}', methods=['PATCH'],dependencies=[Depends(get_current_user)],
                                  endpoint=self.subscriptionTypeRouter.update_subscription_type)
        # self.router.add_api_route(path='/', methods=['DELETE'],
        #                           endpoint=self.storeService.delete_s)

class SubscriptionRouter:
    """
    Router for  subscription 
    """

    def __init__(self):
        """
        Constructor for offertype router
        """
        self.subscriptionRouter = SubscriptionService()
        self.router = APIRouter(prefix='/subscription',tags=['offerType'])
        self.router.add_api_route(path='/{subscription_id:path}', methods=['GET'],dependencies=[Depends(get_current_user)],
                                  endpoint=self.subscriptionRouter.fetch_subscription)
        
        self.router.add_api_route(path='/create', methods=['POST'],dependencies=[Depends(get_current_user)],
                                  endpoint=self.subscriptionRouter.create_subscription)
        self.router.add_api_route(path='/update/{subscription_id:path}', methods=['PATCH'],dependencies=[Depends(get_current_user)],
                                  endpoint=self.subscriptionRouter.update_subscription)

