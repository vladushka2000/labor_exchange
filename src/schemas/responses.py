from typing import Optional

from pydantic import BaseModel


class ResponseSchema(BaseModel):
    id: int = None
    user_id: int
    job_id: int
    message: str

    class Config:
        orm_mode = True


class ResponseUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    is_active: Optional[bool] = None


class ResponseSentSchema(BaseModel):
    job_id: int
    message: str
