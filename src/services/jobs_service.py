import uuid
from typing import Iterable

from dependency_injector.wiring import Provide, inject

from config import app_config, keycloak_config
from models.domain import job
from models.dto import job_dto, jwt_dto
from tools import exceptions, enums
from tools.di_containers import alchemy_container

app_config = app_config.app_config
keycloak_config = keycloak_config.keycloak_config


class JobsService:
    """
    Сервис для работы с Вакансиями
    """

    @inject
    async def get_jobs(
        self,
        limit: int,
        offset: int,
        alchemy_uow=Provide[alchemy_container.AlchemyContainer.uow],
    ) -> Iterable[job.Job]:
        """
        Получить список вакансий
        :param limit: максимум значений
        :param offset: смещение
        :param alchemy_uow: uow для работы с Алхимией
        :return: список вакансий
        """

        async with alchemy_uow as uow:
            jobs = await job.Job.list(uow.session, limit, offset)

            await uow.commit()

            return jobs

    @inject
    async def get_job_by_id(
        self,
        job_id: uuid.UUID,
        alchemy_uow=Provide[alchemy_container.AlchemyContainer.uow],
    ) -> job.Job:
        """
        Получить объект вакансии по ее идентификатору
        :param job_id: идентификатор вакансии
        :param alchemy_uow: uow для работы с Алхимией
        :return: объект вакансии
        """

        async with alchemy_uow as uow:
            job_ = await job.Job.retrieve(uow.session, job_id)

            await uow.commit()

            return job_

    @inject
    async def create_job(
        self, job_: job.Job, alchemy_uow=Provide[alchemy_container.AlchemyContainer.uow]
    ) -> None:
        """
        Создать вакансию
        :param job_: объект вакансии
        :param alchemy_uow: uow для работы с Алхимией
        """

        async with alchemy_uow as uow:
            await job_.create(uow.session)
            await uow.commit()

    @inject
    async def update_job(
        self,
        old_job_id: uuid.UUID,
        user_info: jwt_dto.TokenInfo,
        updated_job: job_dto.UpdatedJob,
        alchemy_uow=Provide[alchemy_container.AlchemyContainer.uow],
    ) -> None:
        """
        Обновить вакансию
        :param old_job_id: идентификатор старой вакансии
        :param user_info: информация о создателе вакансии
        :param updated_job: обновленные данные вакансии
        :param alchemy_uow: uow для работы с Алхимией
        """

        async with alchemy_uow as uow:
            old_job = await job.Job.retrieve(uow.session, old_job_id)

            if (
                old_job.user_id != user_info.id
                and enums.UserRole.ADMIN.name_ not in user_info.roles
            ):
                raise exceptions.PermissionDeniedException()

            old_job.title = updated_job.title
            old_job.description = updated_job.description
            old_job.salary_from = updated_job.salary_from
            old_job.salary_to = updated_job.salary_to
            old_job.is_active = updated_job.is_active

            await old_job.update(uow.session)
            await uow.commit()

    @inject
    async def delete_job(
        self,
        job_id: uuid.UUID,
        user_info: jwt_dto.TokenInfo,
        alchemy_uow=Provide[alchemy_container.AlchemyContainer.uow],
    ) -> None:
        """
        Удалить вакансию
        :param job_id: идентификатор вакансии
        :param user_info: информация о создателе вакансии
        :param alchemy_uow: uow для работы с Алхимией
        """

        async with alchemy_uow as uow:
            job_ = await job.Job.retrieve(uow.session, job_id)

            if (
                job_.user_id != user_info.id
                and enums.UserRole.ADMIN.name_ not in user_info.roles
            ):
                raise exceptions.PermissionDeniedException()

            await job.Job.delete(uow.session, job=job_)
            await uow.commit()
