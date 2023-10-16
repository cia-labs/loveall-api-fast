import logging
from app.utils.logger import api_logger
from app.utils.resp import Resp
from app.models.database import get_session
from app.crud.subscription import SubscriptionDBActions,SubscriptionTypeDBActions
from fastapi import Depends, Request, Body
from sqlalchemy.orm import Session
from starlette.responses import Response
from app.schema.subscription import SubscriptionSchema, SubscriptionTypeSchema
from app.models.user.user import User
from app.models.subscription.subscription import SubscriptionType,Subscription
from app.services.auth.auth_bearer import get_current_user


log = logging.getLogger(__name__)



class SubscriptionTypeService:
    method_decorators = [api_logger]

    def __init__(self):
        self.store_db_actions = None
    
    async def fetch_subscription_type(self, subscription_type_id: str ,request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        try:
            self.store_db_actions = SubscriptionTypeDBActions(db,current_user)
            resp,msg = None,None
            if subscription_type_id and len(subscription_type_id)>0:
                resp, msg =  self.store_db_actions.fetch_subscription_type_by_id(subscription_type_id)
            else:
                resp, msg = self.store_db_actions.fetch_subscription_type()
            if resp:
                log.info(f'SubscriptionType fetched successfully with the name: ')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while fetching the new subscription_type  - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            # log.exception(f'Facing issue while fetching the new user {data.get("name")} - {e}')
            log.exception(f'Facing issue while fetching the new subscription_type  - {e}')
            return Resp.error(response, f'Facing issue in subscription_type -{e}')

    async def create_subscription_type(self,response: Response, subscription_type: SubscriptionTypeSchema = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        try:
            log.info(f'Creating new subscription_type with the data - {subscription_type}')
            self.store_db_actions = SubscriptionTypeDBActions(db,current_user)
            resp, msg = self.store_db_actions.save_new_subscription_type(subscription_type)
            if resp:
                log.info(f'New subscription_type {subscription_type} saved successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while saving the new subscription_type - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while saving the new subscription_type - {e}')
            return Resp.error(response, f'Facing issue in subscription_type -{e}')
    
    async def update_subscription_type(self,subscription_type_id: str,response: Response, subscription_type: SubscriptionTypeSchema = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        # todo : only user to update subscription_type details
        try:
            log.info(f'Updating subscription_type with the data - {subscription_type}')
            self.store_db_actions = SubscriptionTypeDBActions(db,current_user)
            resp, msg = self.store_db_actions.update_subscription_type(subscription_type,subscription_type_id)
            if resp:
                log.info(f'SubscriptionType {subscription_type} updated successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while updating the subscription_type - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while updating the subscription_type - {e}')
            return Resp.error(response, f'Facing issue in subscription_type -{e}')

class SubscriptionService:
    method_decorators = [api_logger]

    def __init__(self):
        self.store_db_actions = None

    async def fetch_subscription(self, subscription_id: str, request: Request, response: Response, db: Session = Depends(get_session),current_user: User= Depends(get_current_user)):
        try:
            
            self.store_db_actions = SubscriptionDBActions(db,current_user)
            resp, msg = None,None
            if subscription_id and len(subscription_id)>0:
                resp, msg =  self.store_db_actions.fetch_subscription_by_id(subscription_id)
            else:
                resp, msg = self.store_db_actions.fetch_subscription()
            if resp:
                log.info(f'Subscription fetched successfully with the name: ')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while fetching the new subscription  - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            # log.exception(f'Facing issue while fetching the new user {data.get("name")} - {e}')
            log.exception(f'Facing issue while fetching the new subscription  - {e}')
            return Resp.error(response, f'Facing issue in subscription -{e}')

    async def create_subscription(self,response: Response, subscription: SubscriptionSchema = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        try:
            log.info(f'Creating new subscription with the data - {subscription}')
            self.store_db_actions = SubscriptionDBActions(db,current_user)
            
            resp, msg = self.store_db_actions.save_new_subscription(subscription)
            if resp:
                log.info(f'New subscription {subscription} saved successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while saving the new subscription - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while saving the new subscription - {e}')
            return Resp.error(response, f'Facing issue in subscription -{e}')
        
    async def update_subscription(self,subscription_id: str,response: Response, subscription: SubscriptionSchema = Body(...),db: Session = Depends(get_session), current_user: User= Depends(get_current_user)):
        # todo : only user to update subscription details
        try:
            log.info(f'Updating subscription with the data - {subscription}')
            self.store_db_actions = SubscriptionDBActions(db)
            resp, msg = self.store_db_actions.update_subscription(subscription,subscription_id)
            if resp:
                log.info(f'Subscription {subscription} updated successfully')
                return Resp.success(response, msg)
            else:
                log.error(f'Facing issue while updating the subscription - {msg}')
                return Resp.error(response, msg)
        except Exception as e:
            log.exception(f'Facing issue while updating the subscription - {e}')
            return Resp.error(response, f'Facing issue in subscription -{e}')
