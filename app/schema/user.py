from pydantic import BaseModel, Field
from datetime import datetime

class UserSchema(BaseModel):
    """
    Defines the schema for the User table
    """
    # id: int
    name: str = Field(description="The user name", examples=["test"])
    email: str = Field(description="The user email", examples=["test@test.com"])
    password: str = Field(description="The user hashed password", examples=["test"],hidden_from_schema=True)
    role: str = Field(description="The user role", examples=["admin"])
    # is_active: bool = Field(description="The user active status", example=True)
    # created_by: str = Field(description="Email of the creator", example="")
    # creation_time: datetime = Field(description="Creation time of the user", example="2021-01-01 00:00:00")
    # modification_time: datetime = Field(description="Modification time of the user", example="2021-01-01 00:00:00")

class UserLoginSchema(BaseModel):
    """
    Defines the schema for the User login
    """
    email: str = Field(description="The user email", examples=["test"])
    password: str = Field(description="The user password", examples=["test"])