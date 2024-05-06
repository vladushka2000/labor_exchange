from pydantic import BaseModel, constr


class ResponseSchema(BaseModel):
    id: str = None
    user_id: str
    job_id: str
    message: constr(min_length=100)

    class Config:
        orm_mode = True


class ResponseInSchema(BaseModel):
    job_id: str
    message: constr(min_length=100)
