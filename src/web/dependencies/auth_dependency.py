from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from models.dto import jwt_dto
from tools.di_containers import service_container

security = HTTPBearer()


def _get_token(token: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Получить токен пользователя
    :param token: токен пользователя из заголовка
    :return: токен пользователя
    """

    return token.credentials


@inject
async def _get_token_info(
    request: Request,
    token: str = Depends(_get_token),
    service=Provide[service_container.ServiceContainer.auth_service],
) -> jwt_dto.TokenInfo:
    """
    Получить информацию о пользователе из токена
    :param request: объект запроса
    :param token: токен
    :param service: объекта сервиса
    :return: информация о пользователе
    """

    token_info = await service.get_token_info(token)
    request.state.token = token
    request.state.token_info = token_info

    return token_info


@inject
async def has_valid_token(
    token_info: jwt_dto.JWTModel = Depends(_get_token_info),
    service=Provide[service_container.ServiceContainer.auth_service],
) -> None:
    """
    Определить, валиден ли токен
    :param token_info: информация о пользователе из токена
    :param service: объект сервиса
    """

    is_valid = service.has_valid_token(token_info)

    if not is_valid:
        raise HTTPException(status_code=403)


@inject
async def is_company(
    token_info: jwt_dto.JWTModel = Depends(_get_token_info),
    service=Provide[service_container.ServiceContainer.auth_service],
) -> None:
    """
    Определить, является ли пользователь компанией по его токену
    :param token_info: информация о пользователе из токена
    :param service: объект сервиса
    """

    is_company_ = service.is_company(token_info)

    if not is_company_:
        raise HTTPException(status_code=403)


@inject
async def is_not_company(
    token_info: jwt_dto.JWTModel = Depends(_get_token_info),
    service=Provide[service_container.ServiceContainer.auth_service],
) -> None:
    """
    Определить, не является ли пользователь компанией по его токену
    :param token_info: информация о пользователе из токена
    :param service: объект сервиса
    """

    is_not_company_ = service.is_not_company(token_info)

    if not is_not_company_:
        raise HTTPException(status_code=403)


@inject
async def is_admin(
    token_info: jwt_dto.JWTModel = Depends(_get_token_info),
    service=Provide[service_container.ServiceContainer.auth_service],
) -> None:
    """
    Определить, является ли пользователь администратором по его токену
    :param token_info: информация о пользователе из токена
    :param service: объект сервиса
    """

    is_admin_ = service.is_admin(token_info)

    if not is_admin_:
        raise HTTPException(status_code=403)
