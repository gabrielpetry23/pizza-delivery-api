from pydantic import BaseModel
from typing import Optional
from pydantic import Field


class SignUpModel(BaseModel):
    id: Optional[int] = Field(default=None)
    username: str
    email: str
    password: str
    is_active: Optional[bool] = Field(default=True)
    is_staff: Optional[bool] = Field(default=False)

    class Config:
        from_attributes = True
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
