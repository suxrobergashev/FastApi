from pydantic import BaseModel
from typing import Optional


class BaseUser(BaseModel):
    username: str
    email: str


class SignUpModel(BaseUser):
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes = True  # Instead of 'orm_mode'
        json_schema_extra = {
            'example': {
                'username': "username",
                'email': "admin@gmail.com",
                'password': "pass4334",
                'is_staff': False,
                'is_active': True
            }
        }


class UserUpdateModel(BaseUser):
    username: Optional[str]
    email: Optional[str]

    class Config:
        from_attributes = True  # Instead of 'orm_mode'
        json_schema_extra = {
            'example': {
                'username': "username",
                'email': "admin@gmail.com",
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = '8516259637e282f2162371b86887406009fe153eea901cc6858697084a277f8b'


class LoginModel(BaseModel):
    username: str
    password: str
