import datetime
import uuid

from pydantic import Field

from interfaces import base_dto


class JWTModel(base_dto.BaseDTO):
    """
    Модель данных JWT-токенов
    """

    access_token: str = Field(description="Access-токен")
    refresh_token: str = Field(description="Refresh-токен")


class TokenInfo(base_dto.BaseDTO):
    """
    Модель данных с информацией asccess-токена
    """

    id: uuid.UUID = Field(description="Идентификатор пользователя")
    is_active: bool = Field(description="Активен ли токен")
    roles: list[str] = Field(description="Роли пользователя")
    email: str = Field(description="Email-адрес")
    username: str = Field(description="Username")
    first_name: str = Field(description="Имя")
    last_name: str = Field(description="Фамилия")
    created_at: datetime.datetime | None = Field(description="Дата регистрации")
