import datetime
from typing import Optional

from pydantic import BaseModel


class JobSchema(BaseModel):
    id: int = None
    user_id: int
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class JobUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    is_active: Optional[bool] = None


class JobSentSchema(BaseModel):
    title: str
    description: str
    salary_from: int
    salary_to: int
    is_active: bool = True
