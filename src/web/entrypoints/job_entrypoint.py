import datetime
import uuid

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request, status

from models.domain import job
from tools.di_containers import service_container
from web.dependencies import auth_dependency
from web.schemas import job_schema

router = APIRouter(prefix="/jobs")


@router.get("/", dependencies=[Depends(auth_dependency.has_valid_token)])
@inject
async def get_jobs(
    limit: int = 100,
    offset: int = 0,
    service=Depends(Provide[service_container.ServiceContainer.jobs_service]),
) -> list[job_schema.JobSchema]:
    """
    Получить список вакансий
    :param limit: максимум значений
    :param offset: смещение
    :param service: объект сервиса
    :return: список компаний
    """

    jobs = await service.get_jobs(limit=limit, offset=offset)

    return [
        job_schema.JobSchema(
            id=job.id,
            user_id=job.user_id,
            title=job.title,
            description=job.description,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
            is_active=job.is_active,
            created_at=job.created_at,
        )
        for job in jobs
    ]


@router.post(
    "/",
    dependencies=[Depends(auth_dependency.is_company)],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_job(
    request: Request,
    job_data: job_schema.UpdatedJobSchema,
    service=Depends(Provide[service_container.ServiceContainer.jobs_service]),
) -> None:
    """
    Получить список вакансий
    :param request: объект запроса
    :param job_data: данные для создания вакансии
    :param service: объект сервиса
    :return: список компаний
    """

    job_ = job.Job(
        id=uuid.uuid4(),
        user_id=request.state.token_info.id,
        title=job_data.title,
        description=job_data.description,
        salary_from=job_data.salary_from,
        salary_to=job_data.salary_to,
        is_active=job_data.is_active,
        created_at=datetime.datetime.now(),
    )

    await service.create_job(job_)


@router.get("/{job_id}", dependencies=[Depends(auth_dependency.has_valid_token)])
@inject
async def get_job_by_id(
    job_id: uuid.UUID,
    service=Depends(Provide[service_container.ServiceContainer.jobs_service]),
) -> job_schema.JobSchema:
    """
    Получить объект вакансии по ее идентификатору
    :param job_id: идентификатор вакансии
    :param service: объект сервиса
    :return: информации о вакансии
    """

    job_ = await service.get_job_by_id(job_id)

    return job_schema.JobSchema(
        id=job_.id,
        user_id=job_.user_id,
        title=job_.title,
        description=job_.description,
        salary_from=job_.salary_from,
        salary_to=job_.salary_to,
        is_active=job_.is_active,
        created_at=job_.created_at,
    )


@router.patch("/{job_id}", dependencies=[Depends(auth_dependency.is_company)])
@inject
async def update_job(
    request: Request,
    job_id: uuid.UUID,
    updated_data: job_schema.UpdatedJobSchema,
    service=Depends(Provide[service_container.ServiceContainer.jobs_service]),
) -> None:
    """
    Получить объект вакансии по ее идентификатору
    :param request: объект запроса
    :param job_id: идентификатор вакансии
    :param updated_data: обновленная информация о вакансии
    :param service: объект сервиса
    :return: информации о вакансии
    """

    await service.update_job(job_id, request.state.token_info, updated_data)


@router.delete(
    "/{job_id}",
    dependencies=[Depends(auth_dependency.is_company)],
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_job(
    request: Request,
    job_id: uuid.UUID,
    service=Depends(Provide[service_container.ServiceContainer.jobs_service]),
) -> None:
    """
    Удалить вакансию по ее идентификатору
    :param request: объект запроса
    :param job_id: идентификатор вакансии
    :param service: объект сервиса
    :return: информации о вакансии
    """

    await service.delete_job(job_id, request.state.token_info)
