import enum
from sqlalchemy import Column, String, DateTime, JSON, Integer, Enum, ForeignKey,func
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime

from app.models.database import Base


class Deployment(enum.Enum):
    SINGLE = 1
    MULTI = 2


class Subscription(Base):
    """
    Defines the DB ORM model for the subscription table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'subscription'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    sub_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(Integer,ForeignKey('user.id', ondelete='cascade'), nullable=False)
    subscription_type_id = Column(Integer,ForeignKey('subscription_type.id', ondelete='cascade'), nullable=False)
    uuid = Column(String(36), unique=True, nullable=False)
    start_date = Column(DateTime, nullable=False, default=func.now())
    end_date = Column(DateTime, nullable=False, default=func.now())
    enabled = Column(Integer, default=0,nullable=False)
    created_by = Column(String(50))
    creation_time = Column(DateTime, nullable=False, default=func.now())
    modification_time = Column(DateTime, nullable=False, default=func.now())
    # todo: add payment data related to subscription later

    def __init__(self, name ,sub_number, customer_id, subscription_type_id, uuid, start_date, end_date, enabled, created_by, creation_time, modification_time):
        """
        Constructor for the Subscription class
        """
        self.name = name
        self.sub_number = sub_number
        self.customer_id = customer_id
        self.subscription_type_id = subscription_type_id
        self.uuid = uuid
        self.start_date = start_date
        self.end_date = end_date
        self.enabled = enabled
        self.created_by = created_by
        self.creation_time = creation_time
        self.modification_time = modification_time



class SubscriptionType(Base):
    """
    Defines the DB ORM model for the subscriptionType table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'subscription_type'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    discount_rate = Column(Integer, nullable=False)
    meta_data = Column(MutableDict.as_mutable(JSON()), nullable=False)
    created_by = Column(String(50))
    creation_time = Column(DateTime, nullable=False, default=func.now())
    modification_time = Column(DateTime, nullable=False, default=func.now())

    def __init__(self, name, description, discount_rate, created_by, creation_time, modification_time):
        """
        Constructor for the SubscriptionType class
        """
        self.name = name
        self.description = description
        self.discount_rate = discount_rate
        self.created_by = created_by
        self.creation_time = creation_time
        self.modification_time = modification_time    