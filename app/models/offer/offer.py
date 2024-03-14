import enum
from sqlalchemy import Column, String, DateTime, JSON, Integer, Enum, ForeignKey, func
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime

from app.models.database import Base

class OfferType(Base):
    """
    Defines the DB ORM model for the offerType table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'offer_type'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    created_by = Column(String(50))
    creation_time = Column(DateTime, nullable=False, default=func.now())
    modification_time = Column(DateTime, nullable=False, default=func.now())
    is_active = Column(Integer, nullable=False, default=1)
    recurrence_pattern = Column(String(255), nullable=True)



    def __init__(self, name, description, created_by, creation_time, modification_time,recurrence_pattern):
            """
            Constructor for the OfferType class
            """
            self.name = name
            self.description = description
            self.created_by = created_by
            self.creation_time = creation_time
            self.modification_time = modification_time
            self.recurrence_pattern = recurrence_pattern

class Offer(Base):
    """
        Defines the DB ORM model for the offer table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'offer'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False, default=func.now())
    end_date = Column(DateTime, nullable=False, default=func.now())
    discount_rate = Column(Integer, nullable=False)
    #minimum_purchase_amount = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False)
    is_active = Column(Integer, nullable=False,default=1)
    offer_type_id = Column(Integer,ForeignKey('offer_type.id', ondelete='cascade'), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id', ondelete='cascade'), nullable=False)
    store_id = Column(Integer,ForeignKey('store.id', ondelete='cascade'), nullable=False)
    subscription_type_id = Column(Integer,ForeignKey('subscription_type.id', ondelete='cascade'), nullable=False)
    created_by = Column(String(50))
    creation_time = Column(DateTime, nullable=False, default=func.now())
    modification_time = Column(DateTime, nullable=False, default=func.now())

    def __init__(self, name, description, start_date, end_date, discount_rate, priority, user_id, enabled, offer_type_id, store_id, created_by, creation_time, modification_time,subscription_type_id):
            """
            Constructor for the Offer class
            """
            self.name = name
            self.description = description
            self.start_date = start_date
            self.end_date = end_date
            self.discount_rate = discount_rate
            self.priority = priority
            self.user_id = user_id
            self.enabled = enabled
            self.offer_type_id = offer_type_id
            self.store_id = store_id
            self.created_by = created_by
            self.creation_time = creation_time
            self.modification_time = modification_time
            self.subscription_type_id = subscription_type_id


