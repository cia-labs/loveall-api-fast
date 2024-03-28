from pydantic import BaseModel, Field
from datetime import datetime
from app.models.transaction import Transaction

class TransactionSchema(BaseModel):
    """
    Defines the schema for the transaction table
    """
    subscription_id: int = Field(description="The transaction subscription_id", examples=["test"])
    # store_id: int = Field(description="The transaction store_id", examples=["test"])
    offer_id: int = Field(description="The transaction offer_id", examples=["test"])
    # user_id: int = Field(description="The transaction user_id", examples=["test"])
    # discount_rate: int = Field(description="The transaction discount_rate", examples=["test"])
    total_amount: int = Field(description="The transaction total_amount", examples=["test"])
    # offer_amount: int = Field(description="The transaction offer_amount", examples=["test"])
    bill_number: str = Field(description="The transaction bill_number", examples=["test"])
    # bill_date: datetime = Field(description="The transaction bill_date", examples=["test"])