from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """
    Класс настроек для приложения
    """

    project_name: str = Field(description="Название проекта", default="labor-exchange")
    app_name: str = Field(description="Название сервиса", default="exchange")
    app_version: str = Field(description="Версия API", default="v1")

    app_host: str = Field(
        description="Хост сервиса",
        default="0.0.0.0",
        alias="PROJECT_HOST",
    )
    app_port: int = Field(
        description="Порт сервиса",
        default="7777",
        alias="PROJECT_PORT",
    )

    okd_stage: str = Field(description="Состояние OKD", default="DEV")

    @property
    def app_dsn(self) -> str:
        """
        Получение url приложения
        :return: dsn
        """

        return str(HttpUrl.build(scheme="http", host=self.host, port=self.port)).rstrip(
            "/"
        )


app_config = Config()
