import datetime
import uuid

from pydantic import Field

from interfaces import base_web_schema


class UserSchema(base_web_schema.BaseWebSchema):
    """
    Модель данных о пользователе
    """

    id: uuid.UUID = Field(description="Идентификатор пользователя")
    username: str = Field(description="Юзернейм")
    first_name: str = Field(description="Имя пользователя")
    last_name: str = Field(description="Фамилия")
    email: str = Field(description="Email пользователя")
    created_at: datetime.datetime = Field(description="Дата регистрации")
