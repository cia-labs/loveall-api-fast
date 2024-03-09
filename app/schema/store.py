from pydantic import BaseModel, Field
from datetime import datetime

class StoreSchema(BaseModel):
    """
    Defines the schema for the store table
    """
    name: str = Field(description="The store name", example="test")
    address: str = Field(description="The store address", example="test")
    meta_data: dict = Field(description="The store metadata", example="test")
    phone: str = Field(description="The store phone", example="test")

class UpdateStoreSchema(BaseModel):
    """
    Defines the schema for the store table
    """
    name: str = Field(description="The store name", example="test")
    address: str = Field(description="The store address", example="test")
    city: str = Field(description="The store city", example="test")
    state: str = Field(description="The store state", example="test")
    zip_code: str = Field(description="The store zip code", example="test")
    phone: str = Field(description="The store phone", example="test")