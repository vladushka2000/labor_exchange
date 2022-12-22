from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db, get_current_user
from models import User
from queries import job as job_queries
from schemas.jobs import JobSchema, JobInSchema, JobUpdateSchema

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobSchema)
async def create_job(
        job: JobInSchema,
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

    return await job_queries.get_all_jobs(db=db, limit=limit, skip=skip)


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

    new_job = await job_queries.update_job(db=db, job=old_job, updated_job=job, current_user=current_user)

    return JobSchema.from_orm(new_job)
