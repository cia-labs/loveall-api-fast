
from sqlalchemy.sql.schema import Column,  ForeignKey
from sqlalchemy.sql.sqltypes import String, DateTime, JSON, Integer
from sqlalchemy.sql.functions import func
from sqlalchemy.ext.mutable import MutableDict
from app.models.database import Base

class Store(Base):
    """
    Defines the DB ORM model for the store table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False)
    phone = Column(String(50), nullable=False)
    merchant_id = Column(Integer,ForeignKey('user.id', ondelete='cascade'), nullable=False)
    created_by = Column(String(50))
    meta_data = Column(MutableDict.as_mutable(JSON()), nullable=False)
    creation_time = Column(DateTime, nullable=False, default=func.now())
    modification_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __init__(self, name, address, phone,merchant_id, created_by, meta_data,creation_time,
                    modification_time):
            """
            Constructor for the Store class
            """
            self.name = name
            self.address = address
            self.phone = phone
            self.merchant_id = merchant_id
            self.created_by = created_by
            self.meta_data = meta_data
            self.creation_time = creation_time
            self.modification_time = modification_time

    def dict(self):
        return {
             "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "merchant_id": self.merchant_id,
            "created_by": self.created_by,
            "meta_data": self.meta_data,
            "creation_time": self.creation_time,
            "modification_time": self.modification_time
        }