from typing import Optional

from abstracts.unit_of_work import UnitOfWork
from dto import UserSchema, UserUpdateSchema
from service.common.utils import filter_dict_none_values


async def get_by_email(
    email: str,
    uow: UnitOfWork,
) -> UserSchema:
    async with uow:
        user = await uow.repository.get_by_email(email)

        if user is None:
            raise ValueError()

        return UserSchema(
            id=str(user.id),
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            is_company=user.is_company,
            created_at=user.created_at
        )


async def get_by_id(
    user_id: str,
    uow: UnitOfWork,
) -> UserSchema:
    async with uow:
        user = await uow.repository.get_by_id(user_id)

        if user is None:
            raise ValueError()

        return UserSchema(
            id=str(user.id),
            name=user.name,
            email=user.email,
            hashed_password=user.hashed_password,
            is_company=user.is_company,
            created_at=user.created_at
        )


async def get_all(
    uow: UnitOfWork,
    is_company: Optional[bool] = None,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
) -> [UserSchema]:
    async with uow:
        users_dto = []
        users_orm = await uow.repository.get_all(is_company, limit, skip)

        for user in users_orm:
            users_dto.append(
                UserSchema(
                    id=str(user.id),
                    name=user.name,
                    email=user.email,
                    hashed_password=user.hashed_password,
                    is_company=user.is_company,
                    created_at=user.created_at
                )
            )

        return users_dto


async def update(
    user_id: str,
    email: str,
    updated_values: UserUpdateSchema,
    uow: UnitOfWork,
) -> UserUpdateSchema:
    async with uow:
        user = await uow.repository.get_by_id(user_id)

        if user is None or user.email != email:
            raise ValueError()

        values_map = updated_values.dict()
        values_map = filter_dict_none_values(values_map)

        await uow.repository.update(user.id, values_map)
        await uow.commit()
        await uow.repository.refresh(user)

        return UserUpdateSchema(
            name=user.name,
            email=user.email,
            is_company=user.is_company
        )
