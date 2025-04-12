from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import app_config, pg_config
from interfaces import base_factory, base_proxy

app_config_ = app_config.app_config
pg_config_ = pg_config.pg_config


class AlchemyConnectionProxy(base_proxy.ConnectionProxy):
    """
    Прокси-соединение для Алхимии
    """

    _session_maker: sessionmaker | None = None
    _session: AsyncSession | None = None

    def __init__(
        self,
        engine_factory: base_factory.BaseFactory,
    ) -> None:
        """
        Инициализировать переменные
        :param engine_factory: фабрика движков для подключения
        """

        self._engine = engine_factory.create()

    @classmethod
    def _connect(cls, engine: AsyncEngine) -> None:
        """
        Установить соединение с БД в рамках HTTP-сессии
        """

        if cls._session_maker is None:
            cls._session_maker = sessionmaker(  # noqa
                autocommit=False,
                autoflush=False,
                bind=engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

        if cls._session is None:
            cls._session = cls._session_maker()

    def connect(self) -> AsyncSession:
        """
        Получить сессию БД
        :return: асинхронная сессия
        """

        self._connect(self._engine)

        return self._session

    async def disconnect(self) -> None:
        """
        Разорвать соединение с БД
        """

        if self._session:
            await self._session.close()
            self._session = None

        self._session_maker = None
