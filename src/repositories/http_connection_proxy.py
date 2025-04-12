import httpx

from interfaces import base_proxy


class HTTPSession(base_proxy.ConnectionProxy):
    """
    Клиент httpx
    """

    def __init__(self) -> None:
        """
        Инициализировать переменные
        """

        self._client = httpx.AsyncClient()

    def connect(self) -> httpx.AsyncClient:
        """
        Получить HTTP-клиент
        """

        return self._client

    async def disconnect(self) -> None:
        """
        Отключить HTTP-клиент
        """

        await self._client.aclose()
