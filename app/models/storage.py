from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from app.models.database import Base
from sqlalchemy.ext.mutable import MutableDict


class Storage(Base):
    """
        Defines the DB ORM model for the storage table
    """
    __bind_key__ = 'loveall'
    __tablename__ = 'storage'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer,ForeignKey('user.id', ondelete='cascade'), nullable=False)
    filename = Column(String(255), nullable=False)
    bucket = Column(String(255), nullable=False)
    meta_data = Column(MutableDict.as_mutable(JSON()), nullable=False)