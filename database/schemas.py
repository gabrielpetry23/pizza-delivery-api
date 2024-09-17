from pydantic import BaseModel
from typing import Optional
from pydantic import Field

class SignUpModel(BaseModel):
    id: Optional[int] = Field(default=None)  # Properly annotate the field with Optional[int]
    username: str
    email: str
    password: str
    is_active: Optional[bool] = Field(default=True)  # Default value using Field
    is_staff: Optional[bool] = Field(default=False)  # Default value using Field
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'username': 'john_doe',
                'email': 'johndoe@gmail.com',
                'password': '123',
                'is_active': True,
                'is_staff': False
            }
        }
