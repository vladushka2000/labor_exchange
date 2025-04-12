from pydantic import Field

from interfaces import base_web_schema


class JWTModel(base_web_schema.BaseWebSchema, base_web_schema.ConfigMixin):
    """
    Модель данных JWT-токенов
    """

    access_token: str = Field(description="Access-токен", alias="accessToken")
    refresh_token: str = Field(description="Refresh-токен", alias="refreshToken")
