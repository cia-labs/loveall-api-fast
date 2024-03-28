import logging
import logging
from app.utils.resp import Resp
from app.models.database import get_session
from app.crud.offer import OfferDBActions,OfferTypeDBActions
from fastapi import Depends, Request, Body
from sqlalchemy.orm import Session
from starlette.responses import Response
from app.schema.offer import OfferSchema,OfferTypeSchema,OfferSchemaUpdate
from app.models.offer import OfferType,Offer
from app.services.auth.auth_bearer import get_current_user
from app.models.user import User


log = logging.getLogger(__name__)

class OfferTypeService:
    

    def __init__(self):
        self.store_db_actions = None

    async def fetch_offer_type(self,offer_type_id: str, request: Request, response: Response, db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        try:
            self.store_db_actions = OfferTypeDBActions(db,current_user)
            resp, msg = None,None
            print(offer_type_id)
            if offer_type_id and len(offer_type_id)>0:
                resp, msg =  self.store_db_actions.fetch_offer_type_by_id(offer_type_id)
            else:
                print(offer_type_id,"ALL")
                resp, msg = self.store_db_actions.fetch_offer_type()
            if resp:
                log.info(f'OfferType fetched successfully with the name: ')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while fetching the new offer_type  - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            # log.exception(f'Facing issue while fetching the new user {data.get("name")} - {e}')
            log.exception(f'Facing issue while fetching the new offer_type  - {e}')
            return Resp.error(response, f'Facing issue in offer_type -{e}')
    
    async def create_offer_type(self,response: Response, offer_type: OfferTypeSchema = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        try:
            log.info(f'Creating new offer_type with the data - {offer_type}')
            self.store_db_actions = OfferTypeDBActions(db,current_user)
            resp, msg = self.store_db_actions.save_new_offer_type(offer_type)
            if resp:
                log.info(f'New offer_type {offer_type} saved successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while saving the new offer_type - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while saving the new offer_type - {e}')
            return Resp.error(response, f'Facing issue in offer_type -{e}')
        
    async def update_offer_type(self,offer_type_id: str,response: Response, offer_type: OfferTypeSchema = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        # todo : only user to update offer_type details
        try:
            log.info(f'Updating offer_type with the data - {offer_type}')
            self.store_db_actions = OfferTypeDBActions(db,current_user)
            resp, msg = self.store_db_actions.update_offer_type(offer_type,offer_type_id)
            if resp:
                log.info(f'OfferType {offer_type} updated successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while updating the offer_type - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while updating the offer_type - {e}')
            return Resp.error(response, f'Facing issue in offer_type -{e}')
        

class OfferService:
    

    def __init__(self):
        self.store_db_actions = None
    
    async def fetch_offer(self, offer_id:str,request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        try:
            self.store_db_actions = OfferDBActions(db,current_user)
            resp, msg = None,None
            if offer_id and len(offer_id)>0:
                resp, msg =  self.store_db_actions.fetch_offer_by_id(offer_id)
            else:
                resp, msg = self.store_db_actions.fetch_offer()
            if resp:
                log.info(f'Offer fetched successfully with the name: ')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while fetching the new offer  - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            # log.exception(f'Facing issue while fetching the new user {data.get("name")} - {e}')
            log.exception(f'Facing issue while fetching the new offer  - {e}')
            return Resp.error(response, f'Facing issue in offer -{e}')

    async def filter_offer(self, request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        try:
            self.store_db_actions = OfferDBActions(db,current_user)
            print(request.json())
            return Resp.success(response, "Offer fetched successfully with the name:")
            # resp, msg = self.store_db_actions.filter_offer()
            # if resp:
            #     log.info(f'Offer fetched successfully with the name: ')
            #     return Resp.success(response, msg)
            # else:
            #     log.error(f'Facing issue while fetching the new offer  - {msg}')
            #     return Resp.error(response, msg)
        except Exception as e:
            # log.exception(f'Facing issue while fetching the new user {data.get("name")} - {e}')
            log.exception(f'Facing issue while fetching the new offer  - {e}')
            return Resp.error(response, f'Facing issue in offer -{e}')

    async def create_offer(self,response: Response, offer: OfferSchema = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        try:
            log.info(f'Creating new offer with the data - {offer}')
            self.store_db_actions = OfferDBActions(db,current_user)
            resp, msg = self.store_db_actions.save_new_offer(offer)
            if resp:
                log.info(f'New offer {offer} saved successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while saving the new offer - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while saving the new offer - {e}')
            return Resp.error(response, f'Facing issue in offer -{e}')

    async def update_offer(self,offer_id: str,response: Response, offer: dict = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        # todo : only user to update offer details
        try:
            log.info(f'Updating offer with the data - {offer}')
            self.store_db_actions = OfferDBActions(db,current_user)
            resp, msg = self.store_db_actions.update_offer(offer,offer_id)
            if resp:
                log.info(f'Offer {offer} updated successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while updating the offer - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while updating the offer - {e}')
            return Resp.error(response, f'Facing issue in offer -{e}')