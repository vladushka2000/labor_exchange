from typing import Optional
import uuid

from abstracts.unit_of_work import UnitOfWork
from dto import UserSchema, ResponseInSchema, ResponseSchema
from repository.alchemy_orm.mappers import JobMapper
from repository.alchemy_orm.models import Response as OrmResponse


async def create(
    response_data: ResponseInSchema,
    user: UserSchema,
    uow: UnitOfWork,
) -> ResponseSchema:
    if user.is_company:
        raise ValueError()

    async with uow:
        job = await uow.repository.get_by_id(response_data.job_id)

        if job is None:
            raise ValueError()

        job = JobMapper.map_orm_to_domain(job)
        job.add_response(uuid.UUID(user.id), response_data.message)

        response = OrmResponse(
            user_id=user.id,
            job_id=response_data.job_id,
            message=response_data.message
        )

        uow.repository.add(response)
        await uow.commit()
        await uow.repository.refresh(response)

        return ResponseSchema(
            id=str(response.id),
            user_id=str(response.user_id),
            job_id=str(response.job_id),
            message=response.message
        )


async def get_users_responses(
    user: UserSchema,
    uow: UnitOfWork,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0
) -> [ResponseSchema]:
    async with uow:
        responses_dto = []
        responses_orm = await uow.repository.get_responses_by_user_id(user.id, limit, skip)

        for response in responses_orm:
            responses_dto.append(
                ResponseSchema(
                    id=str(response.id),
                    user_id=str(response.user_id),
                    job_id=str(response.job_id),
                    message=response.message
                )
            )

        return responses_dto


async def get_responses_by_job_id(
    job_id: str,
    uow: UnitOfWork,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0
) -> [ResponseSchema]:
    async with uow:
        job = await uow.repository.get_by_id(job_id)

        if job is None:
            raise ValueError()

        responses_dto = []
        responses_orm = await uow.repository.get_responses_by_job_id(job_id, limit, skip)

        for response in responses_orm:
            responses_dto.append(
                ResponseSchema(
                    id=str(response.id),
                    user_id=str(response.user_id),
                    job_id=str(response.job_id),
                    message=response.message
                )
            )

        return responses_dto
