from pydantic import BaseModel, Field
from datetime import datetime


class OfferTypeSchema(BaseModel):
    """
    Defines the schema for the offerType table
    """
    name: str = Field(description="The offerType name", example="test")
    description: str = Field(description="The offerType description", example="test")
    recurrence_pattern: str = Field(description="The offerType recurrence pattern", example="test")

class OfferSchema(BaseModel):
    """
    Defines the schema for the offer table
    """
    name: str = Field(description="The offer name", example="test")
    description: str = Field(description="The offer description", example="test")
    start_date: datetime = Field(description="The offer start date", example="test")
    end_date: datetime = Field(description="The offer end date", example="test")
    discount_rate : int = Field(description="The offer discount rate", example="test")
    priority: int = Field(description="The offer priority", example="test")
    offer_type_id: int = Field(description="The offer offer_type_id", example="test")
    store_id: int = Field(description="The offer store_id", example="test")
    subscription_type_id: int = Field(description="The offer subscription_type_id", example="test")

class OfferSchemaUpdate(BaseModel):
    """
    Defines the schema for the offer table
    """
    name: str = Field(description="The offer name", example="test")
    description: str = Field(description="The offer description", example="test")
    start_date: datetime = Field(description="The offer start date", example="test")
    end_date: datetime = Field(description="The offer end date", example="test")
    discount_rate : int = Field(description="The offer discount rate", example="test")
    priority: int = Field(description="The offer priority", example="test")
    is_active : int = Field(description="The offer is_active", example="test")
    offer_type_id: int = Field(description="The offer offer_type_id", example="test")
    store_id: int = Field(description="The offer store_id", example="test")
    subscription_type_id: int = Field(description="The offer subscription_type_id", example="test")








