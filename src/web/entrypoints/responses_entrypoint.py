import uuid

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query, Request, status

from models.domain import response
from tools.di_containers import service_container
from web.dependencies import auth_dependency
from web.schemas import response_schema

router = APIRouter(prefix="/responses")


@router.get("/", dependencies=[Depends(auth_dependency.is_company)])
@inject
async def get_responses_by_job_id(
    request: Request,
    job_id: uuid.UUID = Query(alias="jobId"),
    limit: int = 10,
    offset: int = 0,
    service=Depends(Provide[service_container.ServiceContainer.responses_service]),
) -> list[response_schema.ResponseSchema]:
    """
    Получить список откликов
    :param request: объект запроса
    :param job_id: идентификатор вакансии
    :param limit: максимум значений
    :param offset: смещение
    :param service: объект сервиса
    :return: список компаний
    """

    responses = await service.get_responses_by_job_id(
        job_id, request.state.token_info, limit=limit, offset=offset
    )

    return [
        response_schema.ResponseSchema(
            id=response_.id,
            user_id=response_.user_id,
            job_id=response_.job_id,
            message=response_.message,
        )
        for response_ in responses
    ]


@router.get("/me", dependencies=[Depends(auth_dependency.is_not_company)])
@inject
async def get_my_responses(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    service=Depends(Provide[service_container.ServiceContainer.responses_service]),
) -> list[response_schema.ResponseSchema]:
    """
    Получить список откликов
    :param request: объект запроса
    :param limit: максимум значений
    :param offset: смещение
    :param service: объект сервиса
    :return: список откликов
    """

    responses = await service.get_responses_by_user_id(
        request.state.token_info, limit=limit, offset=offset
    )

    return [
        response_schema.ResponseSchema(
            id=response_.id,
            user_id=response_.user_id,
            job_id=response_.job_id,
            message=response_.message,
        )
        for response_ in responses
    ]


@router.get("/{user_id}", dependencies=[Depends(auth_dependency.is_admin)])
@inject
async def get_user_responses(
    user_id: uuid.UUID,
    limit: int = 10,
    offset: int = 0,
    service=Depends(Provide[service_container.ServiceContainer.responses_service]),
) -> list[response_schema.ResponseSchema]:
    """
    Получить список откликов для пользователя по его идентификатору
    :param user_id: идентификатор пользователя
    :param limit: максимум значений
    :param offset: смещение
    :param service: объект сервиса
    :return: список компаний
    """

    responses = await service.get_responses_by_user_id(
        user_id, limit=limit, offset=offset
    )

    return [
        response_schema.ResponseSchema(
            id=response_.id,
            user_id=response_.user_id,
            job_id=response_.job_id,
            message=response_.message,
        )
        for response_ in responses
    ]


@router.post(
    "/",
    dependencies=[Depends(auth_dependency.is_not_company)],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_response(
    request: Request,
    response_info: response_schema.CreateResponse,
    service=Depends(Provide[service_container.ServiceContainer.responses_service]),
) -> None:
    """
    Создать отклик
    :param request: объект запроса
    :param response_info: информация об отклике
    :param service: объект сервиса
    """

    response_ = response.Response(
        id=uuid.uuid4(),
        user_id=request.state.token_info.id,
        job_id=response_info.job_id,
        message=response_info.message,
    )

    await service.create_response(response_)


@router.patch("/{response_id}", dependencies=[Depends(auth_dependency.is_not_company)])
@inject
async def update_response(
    request: Request,
    response_id: uuid.UUID,
    response_info: response_schema.UpdatedResponse,
    service=Depends(Provide[service_container.ServiceContainer.responses_service]),
) -> None:
    """
    Обновить отклик
    :param request: объект запроса
    :param response_id: идентификатор отклика
    :param response_info: информация об отклике
    :param service: объект сервиса
    """

    await service.update_response(response_id, request.state.token_info, response_info)


@router.delete(
    "/{response_id}",
    dependencies=[Depends(auth_dependency.is_not_company)],
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_response(
    request: Request,
    response_id: uuid.UUID,
    service=Depends(Provide[service_container.ServiceContainer.responses_service]),
) -> None:
    """
    Удалить отклик
    :param request: объект запроса
    :param response_id: идентификатор отклика
    :param service: объект сервиса
    """

    await service.delete_response(response_id, request.state.token_info)
