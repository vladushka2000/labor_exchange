from __future__ import annotations  # noqa

import datetime
import uuid
from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from interfaces import base_alchemy_model


class Job(base_alchemy_model.AlchemyBase, base_alchemy_model.ActiveRecord):
    """
    Модель вакансии
    """

    __tablename__ = "job"
    __table_args__ = {"comment": "Пользователи"}

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, comment="Идентификатор вакансии"
    )
    user_id: Mapped[uuid.UUID] = mapped_column(comment="Идентификатор пользователя")
    title: Mapped[str] = mapped_column(comment="Название вакансии")
    description: Mapped[str] = mapped_column(comment="Описание вакансии")
    salary_from: Mapped[int] = mapped_column(comment="Зарплата от")
    salary_to: Mapped[int] = mapped_column(comment="Зарплата до")
    is_active: Mapped[bool] = mapped_column(comment="Флаг активности вакансии")
    created_at: Mapped[datetime.datetime] = mapped_column(
        comment="Дата публикации вакансии", default=datetime.datetime.now
    )

    async def create(self, session: AsyncSession) -> None:
        """
        Создать объект вакансии
        :param session: сессия Алхимии
        """

        session.add(self)
        await session.flush()

    @staticmethod
    async def retrieve(
        session: AsyncSession,
        job_id: uuid.UUID,
    ) -> Job:
        """
        Получить объект вакансии
        :param session: сессия Алхимии
        :param job_id: идентификатор пользователя
        :return: объект вакансии
        """

        query = select(Job).filter(Job.id == job_id).limit(1)
        result = await session.execute(query)
        job = result.scalars().first()

        if job is None:
            raise ValueError("Объект вакансии не найден")

        return job

    @staticmethod
    async def list(
        session: AsyncSession, limit: int = 10, offset: int = 0
    ) -> Iterable[Job]:
        """
        Получить список объектов вакансии
        :param session: сессия Алхимии
        :param limit: ограничение выборки
        :param offset: пропуск выборки
        :return: список вакансий
        """

        query = select(Job).limit(limit).offset(offset)
        result = await session.execute(query)

        return result.scalars().unique().all()

    async def update(self, session: AsyncSession) -> None:
        """
        Обновить объект вакансии
        :param session: сессия Алхимии
        """

        await session.flush()

    @staticmethod
    async def delete(
        session: AsyncSession, job_id: uuid.UUID | None = None, job: Job | None = None
    ) -> None:
        """
        Удалить объект вакансии
        :param session: сессия Алхимии
        :param job_id: идентификатор вакансии
        :param job: объект вакансии
        """

        if (job_id is None and job is None) or (job_id is not None and job is not None):
            raise ValueError("Нужно передать только один параметр для удаления")

        if job_id:
            query = select(Job).filter(Job.id == job_id).limit(1)
            result = await session.execute(query)
            job = result.scalars().first()

            if job is None:
                raise ValueError("Объект вакансии не найден")

        await session.delete(job)
