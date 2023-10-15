from pydantic import BaseModel, Field
from datetime import datetime


class SubscriptionTypeSchema(BaseModel):
    """
    Defines the schema for the subscriptionType table
    """
    name: str = Field(description="The subscriptionType name", example="test")
    description: str = Field(description="The subscriptionType description", example="test")


class SubscriptionSchema(BaseModel):
    """
    Defines the schema for the subscription table
    """
    name: str = Field(description="The subscription name", example="test")
    sub_number: str = Field(description="The subscription number", example="test")
    user_id : int = Field(description="The subscription user_id", example="test")
    subscription_type_id : int = Field(description="The subscription subscription_type_id", example="test")
    uuid : str = Field(description="The subscription uuid", example="test")
    start_date: datetime = Field(description="The subscription start date", example="test")
    end_date: datetime = Field(description="The subscription end date", example="test")