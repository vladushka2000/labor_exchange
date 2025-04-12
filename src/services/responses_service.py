import uuid
from typing import Iterable

from dependency_injector.wiring import Provide, inject

from config import app_config, keycloak_config
from models.domain import job, response
from models.dto import response_dto, jwt_dto
from tools import exceptions, enums
from tools.di_containers import alchemy_container

app_config = app_config.app_config
keycloak_config = keycloak_config.keycloak_config


class ResponsesService:
    """
    Сервис для работы с Откликами
    """

    @inject
    async def get_responses_by_job_id(
        self,
        job_id: uuid.UUID,
        user_info: jwt_dto.TokenInfo,
        limit: int,
        offset: int,
        alchemy_uow=Provide[alchemy_container.AlchemyContainer.uow],
    ) -> Iterable[response.Response]:
        """
        Получить список откликов
        :param job_id: идентификатор вакансии
        :param user_info: информация о создателе вакансии
        :param limit: максимум значений
        :param offset: смещение
        :param alchemy_uow: uow для работы с Алхимией
        :return: список откликов
        """

        async with alchemy_uow as uow:
            job_ = await job.Job.retrieve(uow.session, job_id)

            if (
                job_.user_id != user_info.id
                and enums.UserRole.ADMIN.name_ not in user_info.roles
            ):
                raise exceptions.PermissionDeniedException()

            responses = await response.Response.list(
                uow.session, job_id=job_id, limit=limit, offset=offset
            )

            await uow.commit()

            return responses

    @inject
    async def get_responses_by_user_id(
        self,
        user_id: uuid.UUID,
        limit: int,
        offset: int,
        alchemy_uow=Provide[alchemy_container.AlchemyContainer.uow],
    ) -> Iterable[response.Response]:
        """
        Получить список откликов
        :param user_id: идентификатор пользователя
        :param limit: максимум значений
        :param offset: смещение
        :param alchemy_uow: uow для работы с Алхимией
        :return: список откликов
        """

        async with alchemy_uow as uow:
            responses = await response.Response.list(
                uow.session, user_id=user_id, limit=limit, offset=offset
            )

            await uow.commit()

            return responses

    @inject
    async def create_response(
        self,
        response_: response.Response,
        alchemy_uow=Provide[alchemy_container.AlchemyContainer.uow],
    ) -> None:
        """
        Создать вакансию
        :param response_: объект отклика
        :param alchemy_uow: uow для работы с Алхимией
        """

        async with alchemy_uow as uow:
            await response_.create(uow.session)
            await uow.commit()

    @inject
    async def update_response(
        self,
        old_response_id: uuid.UUID,
        user_info: jwt_dto.TokenInfo,
        updated_response: response_dto.UpdatedResponse,
        alchemy_uow=Provide[alchemy_container.AlchemyContainer.uow],
    ) -> None:
        """
        Обновить вакансию
        :param old_response_id: идентификатор старого отклика
        :param user_info: данные о создателе отклика
        :param updated_response: обновленные данные отклика
        :param alchemy_uow: uow для работы с Алхимией
        """

        async with alchemy_uow as uow:
            old_response = await response.Response.retrieve(
                uow.session, old_response_id
            )

            if (
                old_response.user_id != user_info.id
                and enums.UserRole.ADMIN.name_ not in user_info.roles
            ):
                raise exceptions.PermissionDeniedException()

            old_response.message = updated_response.message

            await old_response.update(uow.session)
            await uow.commit()

    @inject
    async def delete_response(
        self,
        response_id: uuid.UUID,
        user_info: jwt_dto.TokenInfo,
        alchemy_uow=Provide[alchemy_container.AlchemyContainer.uow],
    ) -> None:
        """
        Удалить отклик
        :param response_id: идентификатор отклика
        :param user_info: данные о создателе отклика
        :param alchemy_uow: uow для работы с Алхимией
        """

        async with alchemy_uow as uow:
            response_ = await response.Response.retrieve(uow.session, response_id)

            if (
                response_.user_id != user_info.id
                and enums.UserRole.ADMIN.name_ not in user_info.roles
            ):
                raise exceptions.PermissionDeniedException()

            await response.Response.delete(uow.session, response=response_)
            await uow.commit()
