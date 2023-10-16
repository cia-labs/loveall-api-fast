import json
import uuid
from datetime import datetime

from app.models.offer.offer import OfferType,Offer
from app.schema.offer import OfferSchema
from app.utils.logger import api_logger
import logging
from app.models.user.user import User



from passlib.context import CryptContext

logger = logging.getLogger(__name__)


class OfferTypeDBActions:
    method_decorators = [api_logger]

    def __init__(self, db,current_user: User):
        self.db = db
        self.current_user = current_user

    def fetch_offer_type(self):
        """
        Fetch offer_type
        """
        try:
            offer_types = self.db.query(OfferType).all()
            if offer_types:
                return True, offer_types
            return True, []
        except Exception as e:
            logger.exception(f'Facing issue while fetching the offer_type - {e}')
            return False, f'Facing issue while fetching the offer_type'
        
    def fetch_offer_type_by_id(self, id: str):
        """
        Fetch offer_type by name
        :param name: Name of the offer_type
        :return: True if success else False
        """
        try:
            offer_types = self.db.query(OfferType).filter(OfferType.id == id).all()
            if offer_types:
                return True, offer_types
            return False, f'OfferType with name {id} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the offer_type with name {id} - {e}')
            return False, f'Facing issue while fetching the offer_type with name {id}'
    
    def save_new_offer_type(self, offer_type: OfferType):
        """
        Save new offer_type
        :param offer_type: New offer_type details
        :return: True if success else False
        """
        try:
            # check if admin
            if not self.current_user.is_superuser():
                return False, f'Only admin can create offer_type'
            self.db.add(OfferType(**offer_type.dict(),**{
                "creation_time":datetime.now(),
                "modification_time": datetime.now(),
                "created_by" :self.current_user.email
            }))
            self.db.commit()
            return True, f'OfferType {offer_type} saved successfully'
        except Exception as e:
            logger.exception(f'Facing issue while saving the new offer_type - {e}')
            return False, f'Facing issue while saving the new offer_type - {e}'
        
    def update_offer_type(self, offer_type: OfferType,offer_type_id: str):
        """
        Update offer_type
        :param offer_type: offer_type details
        :return: True if success else False
        """
        if not self.current_user.is_superuser():
            return False, f'Only admin can update offer_type'
        try:
            result = None
            final_update = {**offer_type.dict(),**{
                "modification_time": datetime.now(),
            }}            
            result = self.db.query(OfferType).filter(OfferType.id == offer_type_id).update(final_update)
            if result==0:
                return False, f'OfferType with id {offer_type_id} not found'
            self.db.commit()
            return True, f'OfferType {offer_type} updated successfully'
        except Exception as e:
            logger.exception(f'Facing issue while updating the offer_type - {e}')
            return False, f'Facing issue while updating the offer_type - {e}'
        


class OfferDBActions:
    method_decorators = [api_logger]

    def __init__(self, db,current_user:User):
        self.db = db
        self.current_user = current_user

    def fetch_offer(self):
        """
        Fetch offer
        """
        try:
            offers = None
            if self.current_user.is_superuser():
                offers = self.db.query(Offer).all()
            else:
                offers = self.db.query(Offer).filter(Offer.user_id == self.current_user.id).all()
            if offers:
                return True, offers
            return True,[]
        except Exception as e:
            logger.exception(f'Facing issue while fetching the offer - {e}')
            return False, f'Facing issue while fetching the offer'

    def fetch_offer_by_id(self, id: int):
        """
        Fetch offer by name
        :param name: Name of the offer
        :return: True if success else False
        """
        try:
            offers = None
            if self.current_user.is_superuser():
                offers = self.db.query(Offer).filter(Offer.id == id).all()
            else:
                offers = self.db.query(Offer).filter(Offer.id == id).filter(Offer.user_id == self.current_user.id).all()
            if offers:
                return True, offers
            return False, f'Offer with name {id} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the offer with name {id} - {e}')
            return False, f'Facing issue while fetching the offer with name {id}'
    
    def save_new_offer(self, offer: OfferSchema):
        """
        Save new offer
        :param offer: New offer details
        :return: True if success else False
        """
        try:
            self.db.add(Offer(**offer.dict(),**{
                "user_id": self.current_user.id,
                "creation_time":datetime.now(),
                "modification_time": datetime.now(),
                "created_by" :self.current_user.email,
                "enabled":0
            }))
            self.db.commit()
            return True, f'Offer {offer} saved successfully'
        except Exception as e:
            logger.exception(f'Facing issue while saving the new offer - {e}')
            return False, f'Facing issue while saving the new offer - {e}'
        
    def update_offer(self, offer: OfferSchema,offer_id: str):
        """
        Update offer
        :param offer: offer details
        :return: True if success else False
        """
        try:
            result = None
            final_update = {**offer.dict(),**{
                "modification_time": datetime.now(),
            }}            
            result = None
            if self.current_user.is_superuser():
                result = self.db.query(Offer).filter(Offer.id == offer_id).update(final_update)
            else:
                result = self.db.query(Offer).filter(Offer.id == offer_id).filter(Offer.user_id == self.current_user.id).update(final_update)
            if result==0:
                return False, f'Offer with id {offer_id} not found'
            self.db.commit()
            return True, f'Offer {offer} updated successfully'
        except Exception as e:
            logger.exception(f'Facing issue while updating the offer - {e}')
            return False, f'Facing issue while updating the offer - {e}'