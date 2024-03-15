from pydantic import BaseModel, Field
from datetime import datetime


class OfferTypeSchema(BaseModel):
    """
    Defines the schema for the offerType table
    """
    name: str = Field(description="The offerType name", examples=["test"])
    description: str = Field(description="The offerType description",examples=["test"])
    recurrence_pattern: str = Field(description="The offerType recurrence pattern",examples=["test"])

class OfferSchema(BaseModel):
    """
    Defines the schema for the offer table
    """
    name: str = Field(description="The offer name", examples=["test"])
    description: str = Field(description="The offer description",examples=["test"])
    start_date: datetime = Field(description="The offer start date",examples=["test"])
    end_date: datetime = Field(description="The offer end date",examples=["test"])
    start_time: str = Field(description="The offer start time",examples=["test"])
    end_time: str = Field(description="The offer end time",examples=["test"])
    discount_rate : int = Field(description="The offer discount rate", examples=["test"])
    priority: int = Field(description="The offer priority",examples=["test"])
    offer_type_id: int = Field(description="The offer offer_type_id",examples=["test"])
    store_id: int = Field(description="The offer store_id", examples=["test"])
    subscription_type_id: int = Field(description="The offer subscription_type_id",examples=["test"])

class OfferSchemaUpdate(BaseModel):
    """
    Defines the schema for the offer table
    """
    name: str = Field(description="The offer name", examples=["test"])
    description: str = Field(description="The offer description", examples=["test"])
    start_date: datetime = Field(description="The offer start date", examples=["test"])
    end_date: datetime = Field(description="The offer end date", examples=["test"])
    start_time: str = Field(description="The offer start time", examples=["test"])
    end_time: str = Field(description="The offer end time", examples=["test"])
    discount_rate : int = Field(description="The offer discount rate", examples=["test"])
    priority: int = Field(description="The offer priority", examples=["test"])
    is_active : int = Field(description="The offer is_active", examples=["test"])
    offer_type_id: int = Field(description="The offer offer_type_id", examples=["test"])
    store_id: int = Field(description="The offer store_id", examples=["test"])
    subscription_type_id: int = Field(description="The offer subscription_type_id", examples=["test"])








