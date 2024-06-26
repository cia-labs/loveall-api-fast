from fastapi import APIRouter
from app.services.store.store import StoreService
from fastapi import FastAPI, Body, Depends
from app.services.auth.auth_bearer import get_current_user

class StoreRouter:
    """
    Router for user
    """

    def __init__(self):
        """
        Constructor for user router
        """
        self.storeService = StoreService()
        self.router = APIRouter(prefix='/store',tags=['Store'])
        self.router.add_api_route(path='/{store_id:path}', methods=['GET'],dependencies=[Depends(get_current_user)],
                                  endpoint=self.storeService.fetch_store)
        
        self.router.add_api_route(path='/create', methods=['POST'],dependencies=[Depends(get_current_user)],
                                  endpoint=self.storeService.create_store)
        self.router.add_api_route(path='/update/{store_id:path}', methods=['PATCH'],dependencies=[Depends(get_current_user)],
                                  endpoint=self.storeService.update_store)
        self.router.add_api_route(path='/upload/{store_id:path}/{images_key:path}', methods=['POST'],dependencies=[Depends(get_current_user)],
                                  endpoint=self.storeService.upload_store_image)
        # self.router.add_api_route(path='/', methods=['DELETE'],
        #                           endpoint=self.storeService.delete_s)


