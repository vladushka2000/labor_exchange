from models import Job, User
from schemas.jobs import JobSentSchema
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status


async def create_job(db: AsyncSession, job_schema: JobSentSchema, current_user: User) -> Job:
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


async def get_all_active_jobs(db: AsyncSession, limit: int = 100, skip: int = 0) -> Optional[List[Job]]:
    query = select(Job).where(Job.is_active).limit(limit).offset(skip)
    res = await db.execute(query)

    return res.scalars().all()


async def get_job_by_id(db: AsyncSession, id: int) -> Optional[Job]:
    query = select(Job).where(Job.id == id).limit(1)
    res = await db.execute(query)

    return res.scalars().first()


async def update_job(db: AsyncSession, job: Job) -> Job:
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job
