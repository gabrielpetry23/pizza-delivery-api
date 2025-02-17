from pydantic import BaseModel, Field, validator
from typing import Optional
from sqlalchemy_utils.types import ChoiceType


class SignUpModel(BaseModel):
    id: Optional[int] = Field(default=None)
    username: str
    email: str
    password: str
    is_active: Optional[bool] = Field(default=True)
    is_staff: Optional[bool] = Field(default=False)

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "johndoe@gmail.com",
                "password": "123",
                "is_active": True,
                "is_staff": False,
            }
        }

class Settings(BaseModel):
        authjwt_secret_key: str = (
            "213eb3751dfa7cebfab46f09ae1154d3e3ab092a4552f0dc3b27099a48a88126"
        )

class LoginModel(BaseModel):
        username: str
        password: str


class OrderModel(BaseModel):
    id: Optional[int] = Field(default=None)
    quantity: int
    order_status: Optional[str] = Field(default="PENDING")
    pizza_size: str = Field(default="SMALL")
    user_id: Optional[int] = Field(default=None)

    @validator("order_status", pre=True, always=True)
    def validate_order_status(cls, v):
        return str(v)

    @validator("pizza_size", pre=True, always=True)
    def validate_pizza_size(cls, v):
        return str(v)

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "quantity": 2,
                "order_status": "PENDING",
                "pizza_size": "SMALL",
                "user_id": 1,
            }
        }