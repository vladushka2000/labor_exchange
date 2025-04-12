import datetime
import uuid

from dependency_injector.wiring import Provide, inject
from http import HTTPStatus

from config import app_config, keycloak_config
from models.domain import user
from models.dto import http_dto
from tools import enums
from tools.di_containers import http_container

app_config = app_config.app_config
keycloak_config = keycloak_config.keycloak_config


class UsersService:
    """
    Сервис для работы с Пользователями
    """

    @inject
    async def get_users(
        self,
        token: str,
        limit: int,
        offset: int,
        is_company: bool = False,
        http_uow=Provide[http_container.HTTPIntegrationContainer.http_async_uow],
    ) -> list[user.User]:
        """
        Получить список пользователей
        :param token: токен
        :param limit: максимум значений
        :param offset: смещение
        :param is_company: флаг вывода компаний
        :param http_uow: uow для http-запросов
        :return: список пользователей
        """

        headers = {}
        headers.update({"Authorization": f"Bearer {token}"})

        group = (
            enums.UserRole.COMPANY.id_ if is_company else enums.UserRole.APPLICANT.id_
        )
        request = http_dto.HTTPRequestDTO(
            url=f"{keycloak_config.keycloak_dsn}/admin/realms/{keycloak_config.realm}/"
            f"groups/{group}/members?first={offset}&max={limit}",
            headers=headers,
        )

        async with http_uow as uow:
            response = await uow.repository.retrieve(request)

            if response.status != HTTPStatus.OK.value:
                raise ConnectionError()

            result = []

            for company in response.payload:
                if (
                    company["username"]
                    == f"service-account-{keycloak_config.client_id}"
                ):
                    continue

                result.append(
                    user.User(
                        id=company["id"],
                        email=company["email"],
                        username=company["username"],
                        first_name=company["firstName"],
                        last_name=company["lastName"],
                        created_at=datetime.datetime.fromtimestamp(
                            company["createdTimestamp"] / 1000
                        ),
                    )
                )

            return result

    @inject
    async def get_user_by_id(
        self,
        token: str,
        user_id: uuid.UUID,
        http_uow=Provide[http_container.HTTPIntegrationContainer.http_async_uow],
    ) -> user.User:
        """
        Получить объект пользователя по его идентификатору
        :param token: токен
        :param user_id: идентификатор пользователя
        :param http_uow: uow для http-запросов
        :return: объект пользователя
        """

        headers = {}
        headers.update({"Authorization": f"Bearer {token}"})

        request = http_dto.HTTPRequestDTO(
            url=f"{keycloak_config.keycloak_dsn}/admin/realms/{keycloak_config.realm}/users/{user_id}",
            headers=headers,
        )

        async with http_uow as uow:
            response = await uow.repository.retrieve(request)

            if response.status != HTTPStatus.OK.value:
                raise ConnectionError()

            return user.User(
                id=response.payload["id"],
                email=response.payload["email"],
                username=response.payload["username"],
                first_name=response.payload["firstName"],
                last_name=response.payload["lastName"],
                created_at=datetime.datetime.fromtimestamp(
                    response.payload["createdTimestamp"] / 1000
                ),
            )
