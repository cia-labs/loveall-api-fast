import enum
from sqlalchemy import Column, String, DateTime, JSON, Integer, Enum, ForeignKey
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
    creation_time = Column(DateTime, nullable=False, default=datetime.now())
    modification_time = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, name, description, created_by, creation_time, modification_time):
            """
            Constructor for the OfferType class
            """
            self.name = name
            self.description = description
            self.created_by = created_by
            self.creation_time = creation_time
            self.modification_time = modification_time

class Offer(Base):
    """
        Defines the DB ORM model for the offer table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'offer'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(50), nullable=False)
    start_date = Column(DateTime, nullable=False, default=datetime.now())
    end_date = Column(DateTime, nullable=False, default=datetime.now())
    priority = Column(Integer, nullable=False)
    enabled = Column(Integer, nullable=False)
    offer_type_id = Column(Integer,ForeignKey('offer_type.id', ondelete='cascade'), nullable=False)

    def __init__(self, name, description, start_date, end_date, priority, enabled, offer_type_id):
            """
            Constructor for the Offer class
            """
            self.name = name
            self.description = description
            self.start_date = start_date
            self.end_date = end_date
            self.priority = priority
            self.enabled = enabled
            self.offer_type_id = offer_type_id