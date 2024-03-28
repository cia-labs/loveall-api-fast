from typing import Any, Dict

import logging
from app.crud.subscription import SubscriptionDBActions
from app.crud.offer import OfferDBActions
from app.models.offer import Offer, OfferType
from app.models.subscription import Subscription, SubscriptionType
import logging
from app.utils.resp import Resp
from app.models.database import get_session
from app.crud.store import StoreDBActions
from fastapi import Depends, Request, Body
from sqlalchemy.orm.session import Session
from starlette.responses import Response
from app.schema.store import StoreSchema
from app.models.user import Store, User
from app.services.auth.auth_bearer import get_current_user


log = logging.getLogger(__name__)


class SearchService:
    

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
        
    async def search_listing(self, \
                            request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        object_map = {
            "offer" : Offer,
            "store" : Store,
            "offer_type": OfferType,
            "subscription_type" : SubscriptionType
        }

        query_keys = request.query_params.keys()
        nested_queries = []
        # filtering based on "-" is presnet in array
        for qkey in list(filter(lambda k: '-' in k, query_keys)):
            key_name, key_val = qkey.split('-')
            if object_map.get(key_name):
                nested_queries.append(self.query_params_to_filter({key_val:request.query_params._dict[qkey]}, object_map[key_name])[0])

        query = self.query_params_to_filter(request.query_params._dict, Store) + nested_queries
        default_conditon : str= "or"
        if request.query_params.get("cond"):
            default_conditon = request.query_params.get("cond")  # type: ignore
        self.search_db_actions =  StoreDBActions(db,current_user)
        resp, msg = self.search_db_actions.filter_listing_store(query,cond=default_conditon)
        if resp:
            log.info(f'Store fetched successfully with the name: ')
            return Resp.success(response, msg)
        else:
            log.error(f'Facing issue while fetching the new store  - {msg}')
            return Resp.error(response, msg)


    async def search_subscription(self, \
                            request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        object_map = {
                "user": User,
                "subscription_type" : SubscriptionType
            }
        query_keys = request.query_params.keys()
        nested_queries = []
        # filtering based on "-" is presnet in array
        for qkey in list(filter(lambda k: '-' in k, query_keys)):
            key_name, key_val = qkey.split('-')
            if object_map.get(key_name):
                nested_queries.append(self.query_params_to_filter({key_val:request.query_params._dict[qkey]}, object_map[key_name])[0])

        query = self.query_params_to_filter(request.query_params._dict, Subscription) + nested_queries
        default_conditon : str= "or"
        if request.query_params.get("cond"):
            default_conditon = request.query_params.get("cond")  # type: ignore
        self.search_db_actions =  SubscriptionDBActions(db,current_user)
        print(query)
        resp, msg = self.search_db_actions.filter_subscription(query,cond=default_conditon)
        if resp:
            log.info(f'Subscription fetched successfully with the name: ')
            return Resp.success(response, msg)
        else:
            log.error(f'Facing issue while fetching the new subscription  - {msg}')
            return Resp.error(response, msg)
