from typing import Any, Dict

import logging
from app.crud.offer import OfferDBActions
from app.models.offer.offer import Offer
from app.utils.logger import api_logger
from app.utils.resp import Resp
from app.models.database import get_session
from app.crud.store import StoreDBActions
from fastapi import Depends, Request, Body
from sqlalchemy.orm import Session
from starlette.responses import Response
from app.schema.store import StoreSchema
from app.models.user.user import Store, User
from app.services.auth.auth_bearer import get_current_user


log = logging.getLogger(__name__)


class SearchService:
    method_decorators = [api_logger]

    def __init__(self):
        self.search_db_actions = None

    def query_params_to_filter(self,query_params: Dict[str, Any] , model: Any) -> list[Any]:
        filters = []
        for field, value in query_params.items():
            if hasattr(model, field):
                filters.append(getattr(model, field).contains(value))
        return filters


    # search offers based on query params
    async def search_offers(self, \
                            request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        query = self.query_params_to_filter(request.query_params._dict, Offer)
        self.search_db_actions =  OfferDBActions(db,current_user)
        resp, msg = self.search_db_actions.filter_offer(query)
        if resp:
            log.info(f'Offer fetched successfully with the name: ')
            return Resp.success(response, msg) # type: ignore
        else:
            log.error(f'Facing issue while fetching the new offer  - {msg}')
            return Resp.error(response, msg) # type: ignore
    
    # search stores based on query params
    async def search_stores(self, \
                            request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        query = self.query_params_to_filter(request.query_params._dict, Store)
        self.search_db_actions =  StoreDBActions(db,current_user)
        resp, msg = self.search_db_actions.filter_store(query)
        if resp:
            log.info(f'Store fetched successfully with the name: ')
            return Resp.success(response, msg)
        else:
            log.error(f'Facing issue while fetching the new store  - {msg}')
            return Resp.error(response, msg)
