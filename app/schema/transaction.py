from pydantic import BaseModel, Field
from datetime import datetime
from app.models.transaction.transaction import Transaction

class TransactionSchema(BaseModel):
    """
    Defines the schema for the transaction table
    """
    subscription_id: int = Field(description="The transaction subscription_id", example="test")
    # store_id: int = Field(description="The transaction store_id", example="test")
    offer_id: int = Field(description="The transaction offer_id", example="test")
    # user_id: int = Field(description="The transaction user_id", example="test")
    # discount_rate: int = Field(description="The transaction discount_rate", example="test")
    total_amount: int = Field(description="The transaction total_amount", example="test")
    # offer_amount: int = Field(description="The transaction offer_amount", example="test")
    bill_number: str = Field(description="The transaction bill_number", example="test")
    # bill_date: datetime = Field(description="The transaction bill_date", example="test")