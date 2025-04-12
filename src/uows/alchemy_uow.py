from __future__ import annotations  # noqa

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from interfaces import base_proxy, base_uow


class AlchemyUOW(base_uow.BaseAsyncUOW):
    """
    UOW для работы с моделями Алхимии
    """

    def __init__(self, connection_proxy: base_proxy.ConnectionProxy) -> None:
        """
        Инициализировать переменные
        :param connection_proxy: прокси сессии Алхимии
        """

        self._transaction: AsyncSessionTransaction | None = None
        self._is_transaction_commited = False
        self._connection_proxy = connection_proxy

        self.session: AsyncSession | None = None

    async def __aenter__(self) -> AlchemyUOW:
        """
        Войти в контекстный менеджер
        :return: объект UOW
        """

        self._transaction = await self._connection_proxy.connect().begin()
        self._is_transaction_commited = False
        self.session = self._connection_proxy.connect()

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        """
        Сделать откат изменений
        """

        await self.rollback()

    async def commit(self) -> None:
        """
        Сделать коммит изменений
        """

        if self._transaction is None:
            raise ValueError("Объект транзакции не инициализирована")

        await self._transaction.commit()
        self._is_transaction_commited = True

    async def rollback(self) -> None:
        """
        Сделать откат изменений
        """

        if self._transaction is None:
            raise ValueError("Объект транзакции не инициализирована")

        if not self._is_transaction_commited:
            await self._transaction.rollback()

        await self._connection_proxy.disconnect()
