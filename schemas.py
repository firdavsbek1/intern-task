from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes=True
        json_schema_extra = {
            'example':{
                'id':13,
                'username':'username',
                'email':'email@gmail.com',
                'password':"********",
                'is_staff':False,
                'is_active':True,
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = 'YOUR SECRET JWT KEY'


class LoginModel(BaseModel):
    username_or_email: str
    password: str
