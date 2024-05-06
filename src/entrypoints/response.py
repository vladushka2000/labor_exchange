from typing import Optional

from fastapi import APIRouter, Depends

from .dependencies import UserDependencies
from dto import ResponseInSchema, ResponseSchema
from repository.alchemy_orm import OrmJobRepository, OrmUserRepository
from service import response as response_service, user as user_service
from unit_of_work import AlchemyOrmUnitOfWork

router = APIRouter(prefix="/responses", tags=["responses"])


@router.post("/create", response_model=ResponseSchema)
async def create_response(
    response: ResponseInSchema,
    user_email: str = Depends(UserDependencies.get_user_email)
) -> ResponseSchema:
    user = await user_service.get_by_email(user_email, AlchemyOrmUnitOfWork(OrmUserRepository))

    return await response_service.create(response, user, AlchemyOrmUnitOfWork(OrmJobRepository))


@router.get("/my_responses", response_model=list[ResponseSchema])
async def get_my_responses(
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
    user_email: str = Depends(UserDependencies.get_user_email)
) -> list[ResponseSchema]:
    user = await user_service.get_by_email(user_email, AlchemyOrmUnitOfWork(OrmUserRepository))

    return await response_service.get_users_responses(user, AlchemyOrmUnitOfWork(OrmJobRepository), limit, skip)


@router.get("", response_model=list[ResponseSchema])
async def get_my_responses(
    job_id: str,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
    user_email: str = Depends(UserDependencies.get_user_email)
) -> list[ResponseSchema]:
    return await response_service.get_responses_by_job_id(job_id, AlchemyOrmUnitOfWork(OrmJobRepository), limit, skip)
