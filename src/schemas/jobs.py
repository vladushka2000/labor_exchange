import datetime
from typing import Optional

from pydantic import BaseModel, validator, conint, constr


class JobSchema(BaseModel):
    id: int = None
    user_id: int
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
    is_active: Optional[bool] = True

    @validator("salary_from")
    def salary_from_16242(cls, v, values, **kwargs):
        if v < 16242:
            raise ValueError(
                "Минимальная зарплата начинается с 16242 руб. "
                "(согласно Федеральному закону от 19.12.2022 N 522-Ф3)"
            )

        return v

    @validator("salary_to")
    def salary_to_greater_or_equals_salary_from(cls, v, values, **kwargs):
        if "salary_from" in values and v < values["salary_from"]:
            raise ValueError("Максимальная зарплата должна быть больше или равна минимальной")

        return v


class JobInSchema(BaseModel):
    title: constr(min_length=10)
    description: constr(min_length=100)
    salary_from: conint(ge=16242)
    salary_to: conint(ge=16242)
    is_active: bool = True

    @validator("salary_from")
    def salary_from_16242(cls, v, values, **kwargs):
        if v < 16242:
            raise ValueError(
                "Минимальная зарплата начинается с 16242 руб. "
                "(согласно Федеральному закону от 19.12.2022 N 522-Ф3)"
            )

        return v

    @validator("salary_to")
    def salary_to_greater_or_equals_salary_from(cls, v, values, **kwargs):
        if "salary_from" in values and v < values["salary_from"]:
            raise ValueError("Максимальная зарплата должна быть больше или равна минимальной")

        return v
