import uuid
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from repository import UserRepository
from .models import User


class OrmUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    def add(self, user: User) -> None:
        self.session.add(user)

    async def refresh(self, user: User) -> None:
        await self.session.refresh(user)

    async def get_by_id(self, user_id: str) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)

        return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)

        return result.scalars().first()

    async def get_all(
        self,
        is_company: Optional[bool] = None,
        limit: Optional[int] = 100,
        skip: Optional[int] = 0
    ) -> [User]:
        query = select(User).limit(limit).offset(skip)

        if is_company is True:
            query = query.where(User.is_company.is_(True))
        elif is_company is False:
            query = query.where(User.is_company.is_(False))

        result = await self.session.execute(query)

        return result.unique().scalars().all()

    async def update(self, user_id: uuid, values_to_update: dict) -> None:
        query = (
            update(User).
            where(User.id == user_id).
            values(**values_to_update).
            returning(User)
        )
        await self.session.execute(query)
