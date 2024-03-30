from pydantic import BaseModel, Field
from datetime import datetime

class UserSchema(BaseModel):
    """
    Defines the schema for the User table
    """
    # id: int
    name: str = Field(description="The user name", examples=["test"])
    email: str = Field(description="The user email", examples=["test@test.com"])
    password: str = Field(description="The user hashed password", examples=["test_password"],hidden_from_schema=True)
    role: str = Field(description="The user role", examples=["customer"])

class UserRegister(BaseModel):
    """
    Defines the schema for the User table
    """
    # id: int
    name: str = Field(description="The user name", examples=["test"])
    email: str = Field(description="The user email", examples=["test@test.com"])
    password: str = Field(description="The user hashed password", examples=["test_password"],hidden_from_schema=True)
    # role: Optional[str] = Field(description="The user role", examples=["customer"])

class UserResponse(BaseModel):
    """
    Defines the schema for the User response
    """
    id: int = Field(description="The user id", examples=[1])
    name: str = Field(description="The user name", examples=["test"])
    email: str = Field(description="The user email", examples=["test@test.com"])
    role: str = Field(description="The user role", examples=["customer"])
    is_active: bool = Field(description="The user active status", examples=[True])

class UserLoginSchema(BaseModel):
    """
    Defines the schema for the User login
    """
    email: str = Field(description="The user email", examples=["test@test.com"])
    password: str = Field(description="The user password", examples=["test_password"])