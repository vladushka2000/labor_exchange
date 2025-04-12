from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Form, Request, status, Query
from fastapi.responses import RedirectResponse

from tools.di_containers import service_container
from web.dependencies import auth_dependency
from web.schemas import auth_schema

router = APIRouter(prefix="/auth")


@router.get("/sign-up")
@inject
async def sign_up(
    service=Depends(Provide[service_container.ServiceContainer.auth_service]),
) -> RedirectResponse:
    """
    Зарегистрироваться в приложении
    :param service: объект сервиса
    :return: редирект на страницу регистрации
    """

    redirect_url = service.get_sign_up_redirect_url()

    return RedirectResponse(url=redirect_url)


@router.get("/sign-in")
@inject
async def sign_in(
    service=Depends(Provide[service_container.ServiceContainer.auth_service]),
) -> RedirectResponse:
    """
    Войти в приложение
    :param service: объект сервиса
    :return: редирект на страницу входа
    """

    redirect_url = service.get_sign_in_redirect_url()

    return RedirectResponse(url=redirect_url)


@router.post("/tokens")
@inject
async def get_tokens(
    code: str = Form(...),
    service=Depends(Provide[service_container.ServiceContainer.auth_service]),
) -> auth_schema.JWTModel:
    """
    Обменять код из Keycloak на токены
    :param code: код из Keycloak
    :param service: объект сервиса
    :return: токены
    """

    tokens = await service.get_tokens(code)

    return auth_schema.JWTModel(
        access_token=tokens.access_token, refresh_token=tokens.refresh_token
    )


@router.put("/company", dependencies=[Depends(auth_dependency.is_admin)])
@inject
async def change_user_role_to_company(
    request: Request,
    user_id: str = Query(alias="userId"),
    service=Depends(Provide[service_container.ServiceContainer.auth_service]),
) -> None:
    """
    Изменить роль пользователя на Компанию
    :param request: объект запроса
    :param user_id: идентификатор пользователя
    :param service: объект сервиса
    """

    await service.change_user_role_to_company(
        user_id, request.state.token, change_to_company=True
    )


@router.delete(
    "/company",
    dependencies=[Depends(auth_dependency.is_admin)],
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def change_user_role_from_company(
    request: Request,
    user_id: str = Query(alias="userId"),
    service=Depends(Provide[service_container.ServiceContainer.auth_service]),
) -> None:
    """
    Отозвать роль Компании для пользователя
    :param request: объект запроса
    :param user_id: идентификатор пользователя
    :param service: объект сервиса
    """

    await service.change_user_role_to_company(
        user_id, request.state.token, change_to_company=False
    )
