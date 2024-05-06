import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr, field_validator, ValidationInfo


class UserSchema(BaseModel):
    id: str = None
    name: constr(min_length=2)
    email: EmailStr
    hashed_password: str
    is_company: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    name: Optional[constr(min_length=2)] = None
    email: Optional[EmailStr] = None
    is_company: Optional[bool] = None


class UserInSchema(BaseModel):
    name: constr(min_length=2)
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False

    @field_validator("password2")
    @classmethod
    def password_match(cls, v: str, info: ValidationInfo, **kwargs) -> bool:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Пароли не совпадают!")

        return True
