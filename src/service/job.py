from typing import Optional

from abstracts.unit_of_work import UnitOfWork
from dto import JobInSchema, JobSchema, JobUpdateSchema, UserSchema
from repository.alchemy_orm.models import Job as OrmJob
from service.common.utils import filter_dict_none_values


async def create(
    job_data: JobInSchema,
    company: UserSchema,
    uow: UnitOfWork,
) -> JobSchema:
    if not company.is_company:
        raise ValueError()

    async with uow:
        job = OrmJob(
            user_id=company.id,
            title=job_data.title,
            description=job_data.description,
            salary_from=job_data.salary_from,
            salary_to=job_data.salary_to,
            is_active=job_data.is_active
        )

        uow.repository.add(job)
        await uow.commit()
        await uow.repository.refresh(job)

        return JobSchema(
            id=str(job.id),
            user_id=str(job.user_id),
            title=job.title,
            description=job.description,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
            is_active=job.is_active,
            created_at=job.created_at
        )


async def get_by_id(
    job_id: str,
    uow: UnitOfWork,
) -> JobSchema:
    async with uow:
        job = await uow.repository.get_by_id(job_id)

        if job is None:
            raise ValueError()

        return JobSchema(
            id=str(job.id),
            user_id=str(job.user_id),
            title=job.title,
            description=job.description,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
            is_active=job.is_active,
            created_at=job.created_at
        )


async def get_all(
    uow: UnitOfWork,
    is_active: Optional[bool] = None,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
) -> [JobSchema]:
    async with uow:
        jobs_dto = []
        jobs_orm = await uow.repository.get_all(limit, skip, is_active)

        for job in jobs_orm:
            jobs_dto.append(
                JobSchema(
                    id=str(job.id),
                    user_id=str(job.user_id),
                    title=job.title,
                    description=job.description,
                    salary_from=job.salary_from,
                    salary_to=job.salary_to,
                    is_active=job.is_active,
                    created_at=job.created_at
                )
            )

        return jobs_dto


async def update(
    job_id: str,
    updated_values: JobUpdateSchema,
    company: UserSchema,
    uow: UnitOfWork,
) -> JobUpdateSchema:
    if not company.is_company:
        raise ValueError()

    async with uow:
        job = await uow.repository.get_by_id(job_id)

        if company.id != str(job.user_id):
            raise ValueError()

        values_map = updated_values.dict()
        values_map = filter_dict_none_values(values_map)

        await uow.repository.update(job_id, values_map)
        await uow.commit()
        await uow.repository.refresh(job)

        return JobUpdateSchema(
            title=job.title,
            description=job.description,
            salary_from=job.salary_from,
            salary_to=job.salary_to,
            is_active=job.is_active
        )
