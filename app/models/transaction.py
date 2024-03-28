from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy.sql.functions import func
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
    discount_rate = Column(Integer, nullable=False)
    customer_id = Column(Integer,ForeignKey('user.id', ondelete='cascade'), nullable=False)
    merchant_id = Column(Integer,ForeignKey('user.id', ondelete='cascade'), nullable=False)
    total_amount = Column(Integer, nullable=False)
    offer_amount = Column(Integer, nullable=False)
    bill_number = Column(String(50), nullable=False)
    bill_date = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(String(50))
    creation_time = Column(DateTime, nullable=False, default=func.now())
    modification_time = Column(DateTime, nullable=False, default=func.now())


    def __init__(self, subscription_id, store_id, offer_id, customer_id, \
                 merchant_id,total_amount, offer_amount, bill_number, created_by, creation_time, modification_time,discount_rate):
        """
        Constructor for the Transaction class
        """
        self.subscription_id = subscription_id
        self.store_id = store_id
        self.offer_id = offer_id
        self.customer_id = customer_id
        self.total_amount = total_amount
        self.merchant_id = merchant_id
        self.offer_amount = offer_amount
        self.bill_number = bill_number
        self.created_by = created_by
        self.creation_time = creation_time
        self.modification_time = modification_time
        self.discount_rate = discount_rate
    
    def dict(self):
        return {
            "id": self.id,
            "subscription_id": self.subscription_id,
            "store_id": self.store_id,
            "offer_id": self.offer_id,
            "customer_id": self.customer_id,
            "merchant_id": self.merchant_id,
            "total_amount": self.total_amount,
            "offer_amount": self.offer_amount,
            "bill_number": self.bill_number,
            "created_by": self.created_by,
            "creation_time": self.creation_time,
            "modification_time": self.modification_time,
            "discount_rate": self.discount_rate
        }

