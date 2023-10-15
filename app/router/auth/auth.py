from fastapi import APIRouter
from app.services.auth.auth import AuthService
from fastapi import FastAPI, Body, Depends
from app.services.auth.auth_bearer import JWTBearer

class AuthRoutes:
    """
    Router for auth
    """
    
    def __init__(self):
        """
        Constructor for auth router
        """
        self.authService = AuthService()
        self.router = APIRouter(prefix='/auth',tags=['Auth'])
        self.router.add_api_route(path='/login', methods=['POST'],
                                endpoint=self.authService.login)
        # self.router.add_api_route(path='/signup', methods=['POST'],
        #                         endpoint=self.userService.create_user)
        # self.router.add_api_route(path='/', methods=['PATCH'],
        #                           endpoint=self.userService.update_user)
        # self.router.add_api_route(path='/', methods=['DELETE'],
        #                           endpoint=self.userService.delete_user)