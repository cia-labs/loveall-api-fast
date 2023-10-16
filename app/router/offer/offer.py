from fastapi import APIRouter
from app.services.offer.offer import OfferService,OfferTypeService
from fastapi import FastAPI, Body, Depends
from app.services.auth.auth_bearer import JWTBearer,get_current_user

class OfferTypeRouter:
    """
    Router for offer type
    """

    def __init__(self):
        """
        Constructor for offertype router
        """
        self.offerTypeRouter = OfferTypeService()
        self.router = APIRouter(prefix='/offerType',tags=['offerType'])
        self.router.add_api_route(path='/{offer_type_id:path}', methods=['GET'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.offerTypeRouter.fetch_offer_type)
        
        self.router.add_api_route(path='/create', methods=['POST'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.offerTypeRouter.create_offer_type)
        self.router.add_api_route(path='/update/{offer_type_id:path}', methods=['PATCH'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.offerTypeRouter.update_offer_type)
        # self.router.add_api_route(path='/', methods=['DELETE'],
        #                           endpoint=self.storeService.delete_s)

class OfferRouter:
    """
    Router for offer type
    """

    def __init__(self):
        """
        Constructor for offertype router
        """
        self.offerRouter = OfferService()
        self.router = APIRouter(prefix='/offer',tags=['offer'])
        self.router.add_api_route(path='/{offer_id:path}', methods=['GET'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.offerRouter.fetch_offer)
        
        # todo: only store owner can add offer based on store_id-user_id
        self.router.add_api_route(path='/create', methods=['POST'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.offerRouter.create_offer)
        self.router.add_api_route(path='/update/{offer_id:path}', methods=['PATCH'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.offerRouter.update_offer)

