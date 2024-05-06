from __future__ import annotations
import abc

from abstracts.repository import Repository


class UnitOfWork(abc.ABC):
    def __init__(self, repository: type[Repository]) -> None:
        self.repository = repository

    async def __aenter__(self) -> UnitOfWork:
        return self

    async def __aexit__(self, *args) -> None:
        await self.rollback()

    @abc.abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
