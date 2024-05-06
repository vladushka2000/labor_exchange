import abc
from typing import Optional
import uuid

from abstracts.repository import Repository, OrmModel


class UserRepository(Repository):
    @abc.abstractmethod
    def add(self, user: OrmModel) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, user_id: uuid) -> OrmModel | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_email(self, email: str) -> OrmModel | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self, limit: Optional[int] = 100, skip: Optional[int] = 0) -> [OrmModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, user_id: uuid, values_to_update: dict) -> None:
        raise NotImplementedError
