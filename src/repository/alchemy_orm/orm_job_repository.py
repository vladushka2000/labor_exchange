import uuid
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from repository import JobRepository
from .models import Job, Response


class OrmJobRepository(JobRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, instance: Job | Response) -> None:
        self.session.add(instance)

    async def refresh(self, job: Job) -> None:
        await self.session.refresh(job)

    async def get_by_id(self, job_id: str) -> Job | None:
        query = select(Job).where(Job.id == job_id)
        result = await self.session.execute(query)

        return result.scalars().first()

    async def get_all(
        self,
        limit: Optional[int] = 100,
        skip: Optional[int] = 0,
        is_active: Optional[bool] = None
    ) -> [Job]:
        query = select(Job).limit(limit).offset(skip)

        if is_active is True:
            query = query.where(Job.is_active.is_(True))
        elif is_active is False:
            query = query.where(Job.is_active.is_(False))

        result = await self.session.execute(query)

        return result.unique().scalars().all()

    async def get_responses_by_user_id(
        self,
        user_id: str,
        limit: Optional[int] = 100,
        skip: Optional[int] = 0
    ) -> [Response]:
        query = select(Response).limit(limit).offset(skip).where(Response.user_id == user_id)
        result = await self.session.execute(query)

        return result.unique().scalars().all()

    async def get_responses_by_job_id(
        self,
        job_id: str,
        limit: Optional[int] = 100,
        skip: Optional[int] = 0
    ) -> [Response]:
        query = select(Response).limit(limit).offset(skip).where(Response.job_id == job_id)
        result = await self.session.execute(query)

        return result.unique().scalars().all()

    async def update(self, job_id: uuid, values_to_update: dict) -> None:
        query = (
            update(Job).
            where(Job.id == job_id).
            values(**values_to_update).
            returning(Job)
        )
        await self.session.execute(query)

    async def delete(self, job: Job) -> None:
        await super().delete(job)
