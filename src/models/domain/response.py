from __future__ import annotations  # noqa

import uuid
from typing import Iterable

from sqlalchemy import ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, joinedload

from interfaces import base_alchemy_model


class Response(base_alchemy_model.AlchemyBase, base_alchemy_model.ActiveRecord):
    """
    Модель отклика
    """

    __tablename__ = "response"
    __table_args__ = {"comment": "Отклики"}

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, comment="Идентификатор отклика"
    )
    user_id: Mapped[uuid.UUID] = mapped_column(comment="Идентификатор пользователя")
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("job.id"), comment="Идентификатор вакансии"
    )
    message: Mapped[str] = mapped_column(comment="Сопроводительное письмо")

    async def create(self, session: AsyncSession) -> None:
        """
        Создать объект отклика
        :param session: сессия Алхимии
        """

        session.add(self)
        await session.flush()

    @staticmethod
    async def retrieve(session: AsyncSession, response_id: uuid.UUID) -> Response:
        """
        Получить объект отклика
        :param session: сессия Алхимии
        :param response_id: идентификатор отклика
        :return: объект отклика
        """

        query = (
            select(Response)
            .filter(Response.id == response_id)
            .options(joinedload(Response.job))
            .limit(1)
        )
        result = await session.execute(query)
        response = result.scalars().first()

        if response is None:
            raise ValueError("Объект отклика не найден")

        return response

    @staticmethod
    async def list(
        session: AsyncSession,
        user_id: uuid.UUID | None = None,
        job_id: uuid.UUID | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> Iterable[Response]:
        """
        Обновить объект отклика
        :param session: сессия Алхимии
        :param user_id: идентификатор пользователя
        :param job_id: идентификатор вакансии
        :param limit: ограничение выборки
        :param offset: пропуск выборки
        :return: список откликов
        """

        if (user_id is not None and job_id is not None) or (
            user_id is None and job_id is None
        ):
            raise ValueError(
                "Для выборки нужен либо идентификатор пользователя, либо идентификатор вакансии"
            )

        query = (
            select(Response)
            .options(joinedload(Response.job))
            .limit(limit)
            .offset(offset)
        )

        if user_id is not None:
            query = query.filter(Response.user_id == user_id)
        elif job_id is not None:
            query = query.filter(Response.job_id == job_id)

        result = await session.execute(query)

        return result.scalars().unique().all()

    async def update(self, session: AsyncSession) -> None:
        """
        Обновить объект отклика
        :param session: сессия Алхимии
        """

        await session.flush()

    @staticmethod
    async def delete(
        session: AsyncSession,
        response_id: uuid.UUID | None = None,
        response: Response | None = None,
    ) -> None:
        """
        Удалить объект вакансии
        :param session: сессия Алхимии
        :param response_id: идентификатор отклика
        :param response: объект отклика
        """

        if (response_id is None and response is None) or (
            response_id is not None and response is not None
        ):
            raise ValueError("Нужно передать только один параметр для удаления")

        if response_id:
            query = select(Response).filter(Response.id == response_id).limit(1)
            result = await session.execute(query)
            response = result.scalars().first()

            if response is None:
                raise ValueError("Объект отклика не найден")

        await session.delete(response)
