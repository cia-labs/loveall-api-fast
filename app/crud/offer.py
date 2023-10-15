import json
import uuid
from datetime import datetime

from app.models.offer.offer import OfferType,Offer
from app.schema.offer import OfferSchema
from app.utils.logger import api_logger
import logging


from passlib.context import CryptContext

logger = logging.getLogger(__name__)


class OfferTypeDBActions:
    method_decorators = [api_logger]

    def __init__(self, db):
        self.db = db

    def fetch_offer_type_by_name(self, name: str):
        """
        Fetch offer_type by name
        :param name: Name of the offer_type
        :return: True if success else False
        """
        try:
            offer_types = self.db.query(OfferType).filter(OfferType.name == name).all()
            if offer_types:
                return True, offer_types
            return False, f'OfferType with name {name} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the offer_type with name {name} - {e}')
            return False, f'Facing issue while fetching the offer_type with name {name}'
    
    def save_new_offer_type(self, offer_type: OfferType):
        """
        Save new offer_type
        :param offer_type: New offer_type details
        :return: True if success else False
        """
        try:
            self.db.add(OfferType(**offer_type.dict(),**{
                "creation_time":datetime.now(),
                "modification_time": datetime.now(),
                "created_by" :""
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
        try:
            self.db.query(OfferType).filter(OfferType.id == offer_type_id).update(offer_type.dict())
            self.db.commit()
            return True, f'OfferType {offer_type} updated successfully'
            return False, f'OfferType with id {offer_type_id} not found'
        except Exception as e:
            logger.exception(f'Facing issue while updating the offer_type - {e}')
            return False, f'Facing issue while updating the offer_type - {e}'
        


class OfferDBActions:
    method_decorators = [api_logger]

    def __init__(self, db):
        self.db = db

    def fetch_offer_by_name(self, name: str):
        """
        Fetch offer by name
        :param name: Name of the offer
        :return: True if success else False
        """
        try:
            offers = self.db.query(Offer).filter(Offer.name == name).all()
            if offers:
                return True, offers
            return False, f'Offer with name {name} not found'
        except Exception as e:
            logger.exception(f'Facing issue while fetching the offer with name {name} - {e}')
            return False, f'Facing issue while fetching the offer with name {name}'
    
    def save_new_offer(self, offer: OfferSchema):
        """
        Save new offer
        :param offer: New offer details
        :return: True if success else False
        """
        try:
            self.db.add(Offer(**offer.dict(),**{
                # "creation_time":datetime.now(),
                # "modification_time": datetime.now(),
                # "created_by" :"",
                "enabled":0
            }))
            self.db.commit()
            return True, f'Offer {offer} saved successfully'
        except Exception as e:
            logger.exception(f'Facing issue while saving the new offer - {e}')
            return False, f'Facing issue while saving the new offer - {e}'
        
    def update_offer(self, offer: Offer,offer_id: str):
        """
        Update offer
        :param offer: offer details
        :return: True if success else False
        """
        try:
            offer = self.db.query(Offer).filter(Offer.id == offer_id).first()
            if offer:
                offer.name = offer.name
                offer.description = offer.description
                offer.start_date = offer.start_date
                offer.end_date = offer.end_date
                offer.priority = offer.priority
                offer.enabled = offer.enabled
                offer.offer_type_id = offer.offer_type_id
                offer.modification_time = datetime.now()
                self.db.commit()
                return True, f'Offer {offer} updated successfully'
            return False, f'Offer with id {offer_id} not found'
        except Exception as e:
            logger.exception(f'Facing issue while updating the offer - {e}')
            return False, f'Facing issue while updating the offer - {e}'