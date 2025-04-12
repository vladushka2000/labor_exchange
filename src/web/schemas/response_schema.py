import uuid

from pydantic import Field

from interfaces import base_web_schema


class UpdatedResponse(base_web_schema.BaseWebSchema):
    """
    Схема обновленных данных для объекта отклика
    """

    message: str = Field(description="Сопроводительное письмо")


class CreateResponse(UpdatedResponse):
    """
    Схема объекта отклика
    """

    job_id: uuid.UUID = Field(description="Идентификатор вакансии")


class ResponseSchema(CreateResponse):
    """
    Схема объекта отклика
    """

    id: uuid.UUID = Field(description="Идентификатор отклика")
    user_id: uuid.UUID = Field(description="Идентификатор пользователя")
