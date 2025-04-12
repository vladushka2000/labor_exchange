import uuid

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request

from tools.di_containers import service_container
from web.dependencies import auth_dependency
from web.schemas import user_schema

router = APIRouter(prefix="/users")


@router.get("/companies", dependencies=[Depends(auth_dependency.has_valid_token)])
@inject
async def get_companies(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    service=Depends(Provide[service_container.ServiceContainer.users_service]),
) -> list[user_schema.UserSchema]:
    """
    Получить список компаний
    :param request: объект запроса
    :param limit: максимум значений
    :param offset: смещение
    :param service: объект сервиса
    :return: список компаний
    """

    companies = await service.get_users(
        request.state.token, limit=limit, offset=offset, is_company=True
    )

    return [
        user_schema.UserSchema(
            id=company.id,
            username=company.username,
            first_name=company.first_name,
            last_name=company.last_name,
            email=company.email,
            created_at=company.created_at,
        )
        for company in companies
    ]


@router.get("/", dependencies=[Depends(auth_dependency.has_valid_token)])
@inject
async def get_users(
    request: Request,
    limit: int = 100,
    offset: int = 0,
    service=Depends(Provide[service_container.ServiceContainer.users_service]),
) -> list[user_schema.UserSchema]:
    """
    Получить список пользователей
    :param request: объект запроса
    :param limit: максимум значений
    :param offset: смещение
    :param service: объект сервиса
    :return: список пользователей
    """

    users = await service.get_users(
        request.state.token, limit=limit, offset=offset, is_company=False
    )

    return [
        user_schema.UserSchema(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            created_at=user.created_at,
        )
        for user in users
    ]


@router.get("/{user_id}", dependencies=[Depends(auth_dependency.has_valid_token)])
@inject
async def get_user_by_id(
    user_id: uuid.UUID,
    request: Request,
    service=Depends(Provide[service_container.ServiceContainer.users_service]),
) -> user_schema.UserSchema:
    """
    Получить объект пользователя по его идентификатору
    :param user_id: идентификатор пользователя
    :param request: объект запроса
    :param service: объект сервиса
    :return: список пользователей
    """

    user = await service.get_user_by_id(request.state.token, user_id)

    return user_schema.UserSchema(
        id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        created_at=user.created_at,
    )
