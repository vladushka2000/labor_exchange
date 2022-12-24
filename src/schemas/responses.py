from pydantic import BaseModel, constr


class ResponseSchema(BaseModel):
    id: int = None
    user_id: int
    job_id: int
    message: constr(min_length=100)

    class Config:
        orm_mode = True


class ResponseInSchema(BaseModel):
    job_id: int
    message: constr(min_length=100)
