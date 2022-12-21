from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.jobs import JobSchema, JobSentSchema, JobUpdateSchema
from dependencies import get_db, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from queries import job as job_queries
from models import User


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobSchema)
async def create_job(
        job: JobSentSchema,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    job = await job_queries.create_job(db=db, job_schema=job, current_user=current_user)

    return JobSchema.from_orm(job)


@router.get("", response_model=JobSchema | List[JobSchema])
async def get_job(
    db: AsyncSession = Depends(get_db),
    id: int = 0,
    limit: int = 100,
    skip: int = 0
):
    if id:
        return await job_queries.get_job_by_id(db=db, id=id)

    return await job_queries.get_all_active_jobs(db=db, limit=limit, skip=skip)


@router.put("", response_model=JobUpdateSchema)
async def update_job(
    id: int,
    job: JobUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    old_job = await job_queries.get_job_by_id(db=db, id=id)

    if old_job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена")
    elif old_job.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Это не ты разместил вакансию")

    old_job.title = job.title if job.title is not None else old_job.title
    old_job.description = job.description if job.description is not None else old_job.description
    old_job.salary_from = job.salary_from if job.salary_to is not None else old_job.salary_from
    old_job.salary_to = job.salary_to if job.salary_to is not None else old_job.salary_to
    old_job.is_active = job.is_active if job.is_active is not None else old_job.is_active

    new_job = await job_queries.update_job(db=db, job=old_job)

    return JobSchema.from_orm(new_job)
