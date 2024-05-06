from typing import Optional

from fastapi import APIRouter, Depends

from .dependencies import UserDependencies
from dto import JobSchema, JobInSchema, JobUpdateSchema
from repository.alchemy_orm import OrmJobRepository, OrmUserRepository
from service import job as job_service, user as user_service
from unit_of_work import AlchemyOrmUnitOfWork

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/create", response_model=JobSchema)
async def create_job(job_data: JobInSchema, user_email: str = Depends(UserDependencies.get_user_email)) -> JobSchema:
    user = await user_service.get_by_email(user_email, AlchemyOrmUnitOfWork(OrmUserRepository))

    return await job_service.create(job_data, user, AlchemyOrmUnitOfWork(OrmJobRepository))


@router.post("/update", response_model=JobUpdateSchema)
async def update_job(
    job_id: str,
    job_data: JobUpdateSchema,
    user_email: str = Depends(UserDependencies.get_user_email)
) -> JobUpdateSchema:
    user = await user_service.get_by_email(user_email, AlchemyOrmUnitOfWork(OrmUserRepository))

    return await job_service.update(job_id, job_data, user, AlchemyOrmUnitOfWork(OrmJobRepository))


@router.get("", response_model=JobSchema | list[JobSchema])
async def get_jobs(
    job_id: Optional[str] = None,
    is_active: Optional[bool] = None,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0
) -> JobSchema | list[JobSchema]:
    if job_id:
        return await job_service.get_by_id(job_id, AlchemyOrmUnitOfWork(OrmJobRepository))

    return await job_service.get_all(AlchemyOrmUnitOfWork(OrmJobRepository), is_active, limit, skip)
