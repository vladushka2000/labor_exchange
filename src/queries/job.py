from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Job, User
from schemas.jobs import JobInSchema, JobUpdateSchema


async def create_job(db: AsyncSession, job_schema: JobInSchema, current_user: User) -> Job:
    if current_user.is_company:
        user_id: int = current_user.id
        job = Job(
            user_id=user_id,
            title=job_schema.title,
            description=job_schema.description,
            salary_from=job_schema.salary_from,
            salary_to=job_schema.salary_to,
            is_active=job_schema.is_active
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)

        return job

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Пользователь не имеет прав :(")


async def get_all_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> Optional[List[Job]]:
    query = select(Job).limit(limit).offset(skip)
    res = await db.execute(query)

    return res.scalars().all()


async def get_job_by_id(db: AsyncSession, id: int) -> Optional[Job]:
    query = select(Job).where(Job.id == id).limit(1)
    res = await db.execute(query)

    return res.scalars().first()


async def update_job(db: AsyncSession, job: Job, updated_job: JobUpdateSchema, current_user: User) -> Job:
    if job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Это не ты разместил вакансию")

    job.title = updated_job.title if updated_job.title is not None else job.title
    job.description = updated_job.description if updated_job.description is not None else job.description
    job.salary_from = updated_job.salary_from if updated_job.salary_to is not None else job.salary_from
    job.salary_to = updated_job.salary_to if updated_job.salary_to is not None else job.salary_to
    job.is_active = updated_job.is_active if updated_job.is_active is not None else job.is_active

    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job
