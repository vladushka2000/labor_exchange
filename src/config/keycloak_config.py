from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings


class KeycloakConfig(BaseSettings):
    """
    Класс настроек для Keycloak
    """

    host_external: str = Field(
        description="Хост Keycloak",
        default="localhost",
        alias="KC_HOSTNAME_EXTERNAL",
    )
    host: str = Field(
        description="Хост Keycloak",
        default="localhost",
        alias="KC_HOSTNAME",
    )
    port: int = Field(
        description="Порт Keycloak",
        default="8080",
        alias="KC_PORT",
    )

    realm: str = Field(
        description="Название realm", default="labor-exchange", alias="KC_REALM_NAME"
    )
    client_id: str = Field(
        description="Идентификатор клиента", default="backend", alias="KC_CLIENT_ID"
    )
    client_secret: str = Field(
        description="Секрет клиента", default="secret", alias="KC_CLIENT_SECRET"
    )

    admin_username: str = Field(
        description="Имя администратора", default="admin", alias="KEYCLOAK_ADMIN"
    )
    admin_password: str = Field(
        description="Пароль администратора",
        default="admin",
        alias="KEYCLOAK_ADMIN_PASSWORD",
    )

    @property
    def external_keycloak_dsn(self) -> str:
        """
        Получение url для внешнего подключения к Keycloak
        :return: dsn
        """

        return str(
            HttpUrl.build(scheme="http", host=self.host_external, port=self.port)
        ).rstrip("/")

    @property
    def keycloak_dsn(self) -> str:
        """
        Получение url для подключения к Keycloak
        :return: dsn
        """

        return str(HttpUrl.build(scheme="http", host=self.host, port=self.port)).rstrip(
            "/"
        )


keycloak_config = KeycloakConfig()
