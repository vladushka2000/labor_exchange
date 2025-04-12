from interfaces import base_uow
from repositories import http_repository


class HTTPUOW(base_uow.BaseAsyncUOW):
    """
    UOW для работы с асинхронными HTTP-репозиториями
    """

    def __init__(self, repository: http_repository.HTTPRepository):
        """
        Инициализировать переменные
        :param repository: асинхронный репозиторий
        """

        self.repository = repository
        super().__init__()

    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        super().commit()

    async def rollback(self) -> None:
        """
        Закрыть сессию
        """

        await self.repository.client.aclose()
