import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator, constr


class UserSchema(BaseModel):
    id: str = None
    name: constr(min_length=1)
    email: EmailStr
    hashed_password: str
    is_company: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: Optional[constr(min_length=1)] = None
    email: Optional[EmailStr] = None
    is_company: Optional[bool] = False


class UserInSchema(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("Пароли не совпадают!")

        return True

