


from fastapi import APIRouter, Depends

from app.services.auth.auth_bearer import JWTBearer, get_current_user
from app.services.search.search import SearchService
from app.services.auth.auth_bearer import JWTBearer,get_current_user



class SearchRouter:
#     """
#     SearchRouter
#     """

    def __init__(self):
        self.searchRouter = SearchService()
        self.router = APIRouter(prefix='/search',tags=['search'])
        self.router.add_api_route(path='/offers', methods=['GET'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                  endpoint=self.searchRouter.search_offers)
        self.router.add_api_route(path='/stores', methods=['GET'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                    endpoint=self.searchRouter.search_stores)
        self.router.add_api_route(path='/listing', methods=['GET'],dependencies=[Depends(JWTBearer()),Depends(get_current_user)],
                                    endpoint=self.searchRouter.search_listing)