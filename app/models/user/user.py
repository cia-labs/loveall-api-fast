import enum
from sqlalchemy import Column, String, DateTime, JSON, Integer, Enum, ForeignKey
from sqlalchemy.ext.mutable import MutableDict
from datetime import datetime

from app.models.database import Base
from app.models.offer.offer import OfferType
from app.models.subscription.subscription import SubscriptionType
from app.models.transaction.transaction import Transaction


class Deployment(enum.Enum):
    SINGLE = 1
    MULTI = 2


class User(Base):
    """
    Defines the DB ORM model for the user table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)
    is_active = Column(Integer, default=0, nullable=False)
    created_by = Column(String(50))
    creation_time = Column(DateTime, nullable=False, default=datetime.now())
    modification_time = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, name, email, password, role, is_active, created_by, creation_time,
                    modification_time):
            """
            Constructor for the User class
            """
            self.name = name
            self.email = email
            self.password = password
            self.role = role
            self.is_active = is_active
            self.created_by = created_by
            self.creation_time = creation_time
            self.modification_time = modification_time

    def get_by_email(email):
        return User.query.filter_by(email=email).first()

class Store(Base):
    """
    Defines the DB ORM model for the store table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id', ondelete='cascade'), nullable=False)
    created_by = Column(String(50))
    creation_time = Column(DateTime, nullable=False, default=datetime.now())
    modification_time = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, name, address, city, state, zip_code, phone, created_by, creation_time,
                    modification_time):
            """
            Constructor for the Store class
            """
            self.name = name
            self.address = address
            self.city = city
            self.state = state
            self.zip_code = zip_code
            self.phone = phone
            self.created_by = created_by
            self.creation_time = creation_time
            self.modification_time = modification_time

