from pydantic import BaseModel, Field
from datetime import datetime

class UserSchema(BaseModel):
    """
    Defines the schema for the User table
    """
    id: int
    name: str = Field(description="The user name", example="test")
    email: str = Field(description="The user email", example="test@test.com")
    password: str = Field(description="The user hashed password", example="test")
    role: str = Field(description="The user role", example="admin")
    is_active: bool = Field(description="The user active status", example=True)
    created_by: str = Field(description="Email of the creator", example="")
    creation_time: datetime = Field(description="Creation time of the user", example="2021-01-01 00:00:00")
    modification_time: datetime = Field(description="Modification time of the user", example="2021-01-01 00:00:00")

class UserLoginSchema(BaseModel):
    """
    Defines the schema for the User login
    """
    email: str = Field(description="The user email", example="")
    password: str = Field(description="The user password", example="")