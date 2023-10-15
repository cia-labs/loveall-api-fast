from fastapi import APIRouter
from app.services.user.user import UserService
from fastapi import FastAPI, Body, Depends
from app.services.auth.auth_bearer import JWTBearer,get_current_user

class UserRouter:
    """
    Router for user
    """

    def __init__(self):
        """
        Constructor for user router
        """
        self.userService = UserService()
        self.router = APIRouter(prefix='/user',tags=['User'])
        self.router.add_api_route(path='/', methods=['GET'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.userService.fetch_user)
        
        self.router.add_api_route(path='/create', methods=['POST'],
                                  endpoint=self.userService.create_user)
        # self.router.add_api_route(path='/', methods=['PATCH'],
        #                           endpoint=self.userService.update_user)
        # self.router.add_api_route(path='/', methods=['DELETE'],
        #                           endpoint=self.userService.delete_user)


