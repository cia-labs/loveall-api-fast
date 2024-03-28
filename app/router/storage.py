from fastapi import APIRouter
from fastapi import FastAPI, Body, Depends
from app.services.auth.auth_bearer import JWTBearer,get_current_user
from app.services.storage.storage import StorageService



class StorageRouter:
    def __init__(self):
        self.storageRoute = StorageService()
        self.router = APIRouter(prefix='/storage',tags=['storage'])
        self.router.add_api_route(path='/upload', methods=['POST'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.storageRoute.upload_file)