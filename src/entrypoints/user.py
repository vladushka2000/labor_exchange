from typing import Optional

from fastapi import APIRouter, Depends

from .dependencies import UserDependencies
from dto import UserUpdateSchema, UserSchema
from repository.alchemy_orm import OrmUserRepository
from service import user as user_service
from unit_of_work import AlchemyOrmUnitOfWork

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/update", response_model=UserUpdateSchema)
async def update_user(
    user_id: str,
    user_data: UserUpdateSchema,
    user_email: str = Depends(UserDependencies.get_user_email)
) -> UserUpdateSchema:
    return await user_service.update(user_id, user_email, user_data, AlchemyOrmUnitOfWork(OrmUserRepository))


@router.get("", response_model=UserSchema | list[UserSchema])
async def get_users(
    user_id: Optional[str] = None,
    is_company: Optional[bool] = None,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0
) -> UserSchema | list[UserSchema]:
    if user_id:
        return await user_service.get_by_id(user_id, AlchemyOrmUnitOfWork(OrmUserRepository))

    return await user_service.get_all(AlchemyOrmUnitOfWork(OrmUserRepository), is_company, limit, skip)
