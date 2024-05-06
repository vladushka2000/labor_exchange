import abc
from typing import Optional
import uuid

from abstracts.repository import Repository, OrmModel


class JobRepository(Repository):
    @abc.abstractmethod
    def add(self, job: OrmModel) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, job_id: uuid) -> OrmModel | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(
        self,
        limit: Optional[int] = 100,
        skip: Optional[int] = 0,
        is_active: Optional[bool] = None
    ) -> [OrmModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, job_id: uuid, values_to_update: dict) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, job: OrmModel) -> None:
        raise NotImplementedError
