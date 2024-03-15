from pydantic import BaseModel, Field
from datetime import datetime

class StoreSchema(BaseModel):
    """
    Defines the schema for the store table
    """
    name: str = Field(description="The store name", examples=["test"])
    description: str = Field(description="The store description", examples=["test"])
    address: str = Field(description="The store address", examples=["test"])
    meta_data: dict = Field(description="The store metadata", examples=["test"])
    phone: str = Field(description="The store phone", examples=["test"])

class UpdateStoreSchema(BaseModel):
    """
    Defines the schema for the store table
    """
    name: str = Field(description="The store name", examples=["test"])
    description: str = Field(description="The store description", examples=["test"])
    address: str = Field(description="The store address", examples=["test"])
    meta_data: dict = Field(description="The store metadata", examples=["test"])
    phone: str = Field(description="The store phone", examples=["test"])