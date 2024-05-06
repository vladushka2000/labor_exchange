import datetime
from typing import Optional

from pydantic import BaseModel, conint, constr, field_validator, ValidationInfo


class JobSchema(BaseModel):
    id: str = None
    user_id: str
    title: constr(min_length=10)
    description: constr(min_length=100)
    salary_from: conint(ge=16242)
    salary_to: conint(ge=16242)
    is_active: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobUpdateSchema(BaseModel):
    title: Optional[constr(min_length=10)] = None
    description: Optional[constr(min_length=100)] = None
    salary_from: Optional[conint(ge=16242)] = None
    salary_to: Optional[conint(ge=16242)] = None
    is_active: Optional[bool] = None

    @field_validator("salary_from")
    @classmethod
    def salary_from_16242(cls, v, values, **kwargs):
        if v < 16242:
            raise ValueError(
                "Минимальная зарплата начинается с 16242 руб. "
                "(согласно Федеральному закону от 19.12.2022 N 522-Ф3)"
            )

        return v

    @field_validator("salary_to")
    @classmethod
    def salary_to_greater_or_equals_salary_from(cls, v, info: ValidationInfo, **kwargs):
        if "salary_from" in info.data and v < info.data["salary_from"]:
            raise ValueError("Максимальная зарплата должна быть больше или равна минимальной")

        return v


class JobInSchema(BaseModel):
    title: constr(min_length=10)
    description: constr(min_length=100)
    salary_from: conint(ge=16242)
    salary_to: conint(ge=16242)
    is_active: Optional[bool] = True

    @field_validator("salary_from")
    @classmethod
    def salary_from_16242(cls, v, values, **kwargs):
        if v < 16242:
            raise ValueError(
                "Минимальная зарплата начинается с 16242 руб. "
                "(согласно Федеральному закону от 19.12.2022 N 522-Ф3)"
            )

        return v

    @field_validator("salary_to")
    @classmethod
    def salary_to_greater_or_equals_salary_from(cls, v, info: ValidationInfo, **kwargs):
        if "salary_from" in info.data and v < info.data["salary_from"]:
            raise ValueError("Максимальная зарплата должна быть больше или равна минимальной")

        return v
