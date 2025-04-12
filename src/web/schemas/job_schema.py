import datetime
import uuid

from pydantic import Field

from interfaces import base_web_schema


class UpdatedJobSchema(base_web_schema.BaseWebSchema):
    """
    Схема обновленных данных для объекта вакансии
    """

    title: str = Field(description="Название вакансии")
    description: str = Field(description="Описание вакансии")
    salary_from: int = Field(description="Зарплата от")
    salary_to: int = Field(description="Зарплата до")
    is_active: bool = Field(description="Флаг активности вакансии")


class JobSchema(UpdatedJobSchema):
    """
    Схема объекта вакансии
    """

    id: uuid.UUID = Field(description="Идентификатор вакансии")
    user_id: uuid.UUID = Field(description="Идентификатор пользователя")
    created_at: datetime.datetime = Field(description="Дата создания")
