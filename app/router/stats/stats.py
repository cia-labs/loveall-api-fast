from fastapi import APIRouter
from app.services.stats.stats import StatsService
from fastapi import FastAPI, Body, Depends
from app.services.auth.auth_bearer import JWTBearer,get_current_user

class StatsRouter:
    """
    Router for user
    """

    def __init__(self):
        """
        Constructor for user router
        """
        self.statsService = StatsService()
        self.router = APIRouter(prefix='/stats',tags=['Stats'])
        self.router.add_api_route(path='/transaction', methods=['GET'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.statsService.transaction_stats)
        
        # self.router.add_api_route(path='/create', methods=['POST'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
        #                           endpoint=self.statsService.create_store)
        # self.router.add_api_route(path='/update/{store_id:path}', methods=['PATCH'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
        #                           endpoint=self.statsService.update_store)
        # self.router.add_api_route(path='/', methods=['DELETE'],
        #                           endpoint=self.statsService.delete_s)