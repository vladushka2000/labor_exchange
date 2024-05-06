from abstracts.repository import Repository
from abstracts.unit_of_work import UnitOfWork
from repository.alchemy_orm.common import SessionMaker


class AlchemyOrmUnitOfWork(UnitOfWork):
    def __init__(self, repository: type[Repository]) -> None:
        super().__init__(repository)
        self.session_maker = SessionMaker

    async def __aenter__(self) -> UnitOfWork:
        self.session = self.session_maker()
        self.repository = self.repository(self.session)

        return await super().__aenter__()

    async def __aexit__(self, *args) -> None:
        await super().__aexit__(*args)
        await self.session.aclose()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
