from pydantic import BaseModel, Field
from datetime import datetime


class SubscriptionTypeSchema(BaseModel):
    """
    Defines the schema for the subscriptionType table
    """
    name: str = Field(description="The subscriptionType name", examples=["test"])
    description: str = Field(description="The subscriptionType description", examples=["test"])
    meta_data: dict = Field(description="The subscriptionType meta_data", examples=["test"])


class SubscriptionSchema(BaseModel):
    """
    Defines the schema for the subscription table
    """
    name: str = Field(description="The subscription name", examples=["test"])
    sub_number: str = Field(description="The subscription number", examples=["test"])
    customer_id : int = Field(description="The subscription user_id", examples=["test"])
    subscription_type_id : int = Field(description="The subscription subscription_type_id", examples=["test"])
    uuid : str = Field(description="The subscription uuid", examples=["test"])
    start_date: datetime = Field(description="The subscription start date", examples=["test"])
    end_date: datetime = Field(description="The subscription end date", examples=["test"])


