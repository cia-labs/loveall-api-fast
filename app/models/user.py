import enum
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String, DateTime, JSON, Integer, Enum
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import deferred
from app.models.database import Base

class Deployment(enum.Enum):
    SINGLE = 1
    MULTI = 2


class UserRole(enum.Enum):
    ADMIN = 'admin'
    CUSTOMER = 'customer'
    MERCHANT = 'merchant'
    ZOMBIE = 'zombie'

class User(Base):
    """
    Defines the DB ORM model for the user table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(30), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    # uses deferred column loading 
    password = deferred(Column(String(255), nullable=False))
    role = Column(Enum(UserRole), nullable=False, default=UserRole.ZOMBIE)
    is_active = Column(Integer, default=0, nullable=False)
    created_by = Column(String(50))
    creation_time = Column(DateTime, nullable=False, default=func.now())
    modification_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __init__(self, name, email, password, role, is_active, created_by, creation_time,
                    modification_time):
            """
            Constructor for the User class
            """
            self.name = name
            self.email = email
            self.password = password
            self.role  = role
            self.is_active = is_active
            self.created_by = created_by
            self.creation_time = creation_time
            self.modification_time = modification_time

    # is superuser
    def is_superuser(self):
        if self.role == UserRole.ADMIN: # type: ignore
            return True
    def is_merchant(self):
        if self.role == UserRole.MERCHANT:
            return True
    def is_customer(self):
        if self.role == UserRole.CUSTOMER:
            return True
    

    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_by": self.created_by,
            "creation_time": self.creation_time,
            "modification_time": self.modification_time
        }