import enum
from sqlalchemy import Column, String, DateTime, JSON, Integer, Enum, ForeignKey
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime

from app.models.database import Base


class Transaction(Base):
    """
        Defines the DB ORM model for the transaction table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    subscription_id = Column(Integer,ForeignKey('subscription.id', ondelete='cascade'), nullable=False)
    store_id = Column(Integer,ForeignKey('store.id', ondelete='cascade'), nullable=False)
    offer_id = Column(Integer,ForeignKey('offer.id', ondelete='cascade'), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id', ondelete='cascade'), nullable=False)
    merchant_user_id = Column(Integer,ForeignKey('user.id', ondelete='cascade'), nullable=False)
    total_amount = Column(Integer, nullable=False)
    offer_amount = Column(Integer, nullable=False)
    bill_number = Column(String(50), nullable=False)
    bill_date = Column(DateTime, nullable=False, default=datetime.now())
    created_by = Column(String(50))
    creation_time = Column(DateTime, nullable=False, default=datetime.now())
    modification_time = Column(DateTime, nullable=False, default=datetime.now())


    def __init__(self, subscription_id, store_id, offer_id, user_id, merchant_user_id,total_amount, offer_amount, bill_number, bill_date, created_by, creation_time, modification_time):
        """
        Constructor for the Transaction class
        """
        self.subscription_id = subscription_id
        self.store_id = store_id
        self.offer_id = offer_id
        self.user_id = user_id
        self.total_amount = total_amount
        self.merchant_user_id = merchant_user_id
        self.offer_amount = offer_amount
        self.bill_number = bill_number
        self.bill_date = bill_date
        self.created_by = created_by
        self.creation_time = creation_time
        self.modification_time = modification_time
        


