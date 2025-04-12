import base64
import datetime
import uuid

from dependency_injector.wiring import Provide, inject
from http import HTTPStatus

from config import app_config, keycloak_config
from models.dto import http_dto, jwt_dto
from tools import const, enums, exceptions
from tools.di_containers import http_container

app_config = app_config.app_config
keycloak_config = keycloak_config.keycloak_config


class AuthService:
    """
    Сервис для аутентификации
    """

    @inject
    async def get_token_info(
        self,
        token: str,
        http_uow=Provide[http_container.HTTPIntegrationContainer.http_async_uow],
    ) -> jwt_dto.TokenInfo:
        """
        Получить информацию о токене
        :param token: токен
        :param http_uow: uow для http-запросов
        :return: True, если только валиден, иначе False
        """

        credentials = f"{keycloak_config.client_id}:{keycloak_config.client_secret}"
        basic_auth = base64.b64encode(credentials.encode()).decode()

        headers = {}
        headers.update(const.HTTPHeaders.FORM_HEADER)
        headers.update({"Authorization": f"Basic {basic_auth}"})

        data = {"token": token, "client_id": keycloak_config.client_id}

        request = http_dto.HTTPRequestDTO(
            url=f"{keycloak_config.keycloak_dsn}/realms/{keycloak_config.realm}/"
            f"protocol/openid-connect/token/introspect",
            headers=headers,
            form_data=data,
        )

        async with http_uow as uow:
            response = await uow.repository.create(request)

            if response.status != HTTPStatus.OK.value:
                raise exceptions.InvalidTokenException()

            try:
                return jwt_dto.TokenInfo(
                    id=uuid.UUID(response.payload["user_id"]),
                    is_active=response.payload["active"],
                    roles=response.payload["realm_roles"],
                    email=response.payload["email"],
                    username=response.payload["username"],
                    first_name=response.payload["given_name"],
                    last_name=response.payload["family_name"],
                    created_at=(
                        datetime.datetime.fromtimestamp(
                            response.payload["createdTimestamp"] / 1000
                        )
                        if response.payload.get("createdTimestamp")
                        else None
                    ),
                )
            except KeyError:
                raise exceptions.InvalidTokenException()

    def has_valid_token(self, token_info: jwt_dto.TokenInfo) -> bool:
        """
        Проверить, имеет пользователь валидный токен
        :param token_info: информация о пользователе из токена
        :return: True, если токен валиден, иначе False
        """

        if not token_info.is_active:
            return False

        return True

    def is_company(self, token_info: jwt_dto.TokenInfo) -> bool:
        """
        Проверить, является ли пользователь компанией
        :param token_info: информация о пользователе из токена
        :return: True, если пользователь является компанией, иначе False
        """

        if self.is_admin(token_info):
            return True

        if (
            not token_info.is_active
            or enums.UserRole.COMPANY.name_ not in token_info.roles
        ):
            return False

        return True

    def is_not_company(self, token_info: jwt_dto.TokenInfo) -> bool:
        """
        Проверить, не является ли пользователь компанией
        :param token_info: информация о пользователе из токена
        :return: True, если пользователь не является компанией, иначе False
        """

        if self.is_admin(token_info):
            return True

        if not token_info.is_active or enums.UserRole.COMPANY.name_ in token_info.roles:
            return False

        return True

    def is_admin(self, token_info: jwt_dto.TokenInfo) -> bool:
        """
        Проверить, является ли пользователь администратором
        :param token_info: информация о пользователе из токена
        :return: True, если пользователь администратор, иначе False
        """

        if (
            not token_info.is_active
            or enums.UserRole.ADMIN.name_ not in token_info.roles
        ):
            return False

        return True

    @inject
    async def change_user_role_to_company(
        self,
        user_id: str,
        admin_token: str,
        change_to_company=True,
        http_uow=Provide[http_container.HTTPIntegrationContainer.http_async_uow],
    ) -> None:
        """
        Поменять роль пользователя
        :param user_id: идентификатор пользователя
        :param admin_token: access-токен администратора
        :param change_to_company: флаг смены на компанию
        :param http_uow: uow для http-запросов
        """

        headers = {}
        headers.update(const.HTTPHeaders.JSON_HEADER)
        headers.update({"Authorization": f"Bearer {admin_token}"})

        request = http_dto.HTTPRequestDTO(
            url=(
                f"{keycloak_config.keycloak_dsn}/admin/realms/"
                f"{keycloak_config.realm}/users/{user_id}/groups/{enums.UserRole.COMPANY.id_}"
            ),
            headers=headers,
        )

        async with http_uow as uow:
            if change_to_company:
                response = await uow.repository.update(request)
            else:
                response = await uow.repository.delete(request)

            if response.status != HTTPStatus.NO_CONTENT.value:
                raise ConnectionError("Роль не была изменена")

    def get_sign_up_redirect_url(self) -> str:
        """
        Получить ссылку на редирект для регистрации
        :return: ссылка на редирект
        """

        return (
            f"{keycloak_config.external_keycloak_dsn}/realms/{keycloak_config.realm}"
            f"/protocol/openid-connect/registrations?"
            f"client_id={keycloak_config.client_id}&response_type=code&response_mode=form_post"
        )

    def get_sign_in_redirect_url(self) -> str:
        """
        Получить ссылку на редирект для входа
        :return: ссылка на редирект
        """

        return (
            f"{keycloak_config.external_keycloak_dsn}/realms/{keycloak_config.realm}/protocol/openid-connect/auth?"
            f"client_id={keycloak_config.client_id}&response_type=code&response_mode=form_post"
        )

    @inject
    async def get_tokens(
        self,
        keycloak_code: str,
        http_uow=Provide[http_container.HTTPIntegrationContainer.http_async_uow],
    ) -> jwt_dto.JWTModel:
        """
        Обменять код Keycloak на access и refresh-токен
        :param keycloak_code: код Keycloak
        :param http_uow: uow для http-запросов
        :return: access и refresh-токены
        """

        tokens_url = (
            f"{keycloak_config.keycloak_dsn}/realms/"
            f"{keycloak_config.realm}/protocol/openid-connect/token"
        )
        headers = {}
        headers.update(const.HTTPHeaders.FORM_HEADER)
        form_data = {
            "client_id": keycloak_config.client_id,
            "client_secret": keycloak_config.client_secret,
            "grant_type": "authorization_code",
            "code": keycloak_code,
        }

        request = http_dto.HTTPRequestDTO(
            url=tokens_url, headers=headers, form_data=form_data
        )

        async with http_uow as uow:
            response = await uow.repository.create(request)

            if response.status != HTTPStatus.OK.value:
                raise ConnectionError("Токены не были получены")

            return jwt_dto.JWTModel(
                access_token=response.payload["access_token"],
                refresh_token=response.payload["refresh_token"],
            )
