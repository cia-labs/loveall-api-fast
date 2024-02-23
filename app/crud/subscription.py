import json
import uuid
from datetime import datetime

from app.models.subscription.subscription import SubscriptionType,Subscription
from app.schema.subscription import SubscriptionSchema,SubscriptionTypeSchema
from app.utils.logger import api_logger
from app.models.user.user import User
import logging

from passlib.context import CryptContext
logger = logging.getLogger(__name__)

class SubscriptionTypeDBActions:
    method_decorators = [api_logger]
    def __init__(self, db,current_user:User):
        self.db = db
        self.current_user = current_user
    
    def fetch_subscription_type_by_id(self, subscription_type_id: str):
        """
        Fetch subscription_type by id
        :param subscription_type_id: id of the subscription_type
        :return: True if success else False
        """
        try:
            subscription_types = self.db.query(SubscriptionType).filter(SubscriptionType.id == subscription_type_id).all()
            if subscription_types:
                return True, subscription_types
            return False, f'SubscriptionType with id {subscription_type_id} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the subscription_type with id {subscription_type_id} - {e}')
            return False, f'Facing issue while fetching the subscription_type with id {subscription_type_id}'
    def fetch_subscription_type(self):
        """
        Fetch subscription_type by name
        :param name: Name of the subscription_type
        :return: True if success else False
        """
        try:
            subscription_types = self.db.query(SubscriptionType).all()
            if subscription_types:
                return True, subscription_types
            return False, f'SubscriptionType  not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the subscription_type - {e}')
            return False, f'Facing issue while fetching the subscription_type'

    def save_new_subscription_type(self, subscription_type: SubscriptionTypeSchema):
        """
        Save new subscription_type
        :param subscription_type: New subscription_type details
        :return: True if success else False
        """
        try:
            if not self.current_user.is_superuser():
                return False, f'Only superuser can create subscription_type'
            self.db.add(SubscriptionType(**subscription_type.dict(),**{
                "creation_time":datetime.now(),
                "modification_time": datetime.now(),
                "created_by" : self.current_user.email,
            }))
            self.db.commit()
            return True, f'SubscriptionType {subscription_type} saved successfully'
        except Exception as e:
            logger.exception(f'Facing issue while saving the new subscription_type - {e}')
            return False, f'Facing issue while saving the new subscription_type - {e}'
    
    def update_subscription_type(self, subscription_type: SubscriptionTypeSchema,subscription_type_id: str):
        """
        Update subscription_type
        :param subscription_type: subscription_type details
        :return: True if success else False
        """
        try:
            if not self.current_user.is_superuser():
                return False, f'Only superuser can update subscription_type'
            self.db.query(SubscriptionType).filter(SubscriptionType.id == subscription_type_id).update(subscription_type.dict())
            self.db.commit()
            return True, f'SubscriptionType {subscription_type} updated successfully'
        except Exception as e:
            logger.exception(f'Facing issue while updating the subscription_type - {e}')
            return False, f'Facing issue while updating the subscription_type - {e}'

class SubscriptionDBActions:
    method_decorators = [api_logger]
    def __init__(self, db,current_user:User):
        self.db = db
        self.current_user = current_user
    
    def fetch_subscription(self,):
        """
        Fetch subscription by name
        :param name: Name of the subscription
        :return: True if success else False
        """
        try:
            if self.current_user.is_superuser() or self.current_user.role == 'merchant':
                subscriptions = self.db.query(Subscription).all()
            else:
                subscriptions = self.db.query(Subscription).filter(Subscription.user_id == self.current_user.id).all()
            if subscriptions:
                return True, subscriptions
            return True, []
        except Exception as e:
            logger.exception(f'Facing issue while fetching the subscription with name {id} - {e}')
            return False, f'Facing issue while fetching the subscription with name {id}'
    
    def fetch_subscription_by_id(self, subscription_id: str):
        """
        Fetch subscription by id
        :param subscription_id: id of the subscription
        :return: True if success else False
        """
        try:
            subscriptions = self.db.query(Subscription).filter(Subscription.id == subscription_id).all()
            if subscriptions:
                return True, subscriptions
            return False, f'Subscription with id {subscription_id} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the subscription with id {subscription_id} - {e}')
            return False, f'Facing issue while fetching the subscription with id {subscription_id}'
        
    def save_new_subscription(self, subscription: SubscriptionSchema):
        """
        Save new subscription
        :param subscription: New subscription details
        :return: True if success else False
        """
        
        try:
            if not self.current_user.is_superuser():
                return False, f'Only superuser can create subscription'
        
            self.db.add(Subscription(**subscription.dict(),**{
                "creation_time":datetime.now(),
                "modification_time": datetime.now(),
                "created_by" :self.current_user.email,
                "enabled":0
            }))
            self.db.commit()
            return True, f'Subscription {subscription} saved successfully'
        except Exception as e:
            logger.exception(f'Facing issue while saving the new subscription - {e}')
            return False, f'Facing issue while saving the new subscription - {e}'
    
    def update_subscription(self, subscription: SubscriptionSchema,subscription_id: str):
        """
        Update subscription
        :param subscription: subscription details
        :return: True if success else False
        """
        try:
            self.db.query(Subscription).filter(Subscription.id == subscription_id).update({
                **subscription.dict(),
                "modification_time": datetime.now(),
            })
            self.db.commit()
            return True, f'Subscription {subscription} updated successfully'
        except Exception as e:
            logger.exception(f'Facing issue while updating the subscription - {e}')
            return False, f'Facing issue while updating the subscription - {e}'
        
