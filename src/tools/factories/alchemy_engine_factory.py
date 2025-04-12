from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from pydantic import PostgresDsn

from config import app_config
from interfaces import base_factory

app_config_ = app_config.app_config


class AlchemyEngineFactory(base_factory.BaseFactory):
    """
    Фабрика движка соединений для реализации Алхимии
    """

    _engine: AsyncEngine | None = None

    def __init__(self, dsn: PostgresDsn, max_size: int) -> None:
        """
        Инициализировать переменные
        :param dsn: postgres dsn
        :param max_size: максимальное количество доступных соединений
        """

        self._dsn = dsn
        self._max_size = max_size

    @classmethod
    def _create(cls, dsn: PostgresDsn, max_size: int, **kwargs) -> AsyncEngine:
        """
        Создать единственный движок соединений
        :param dsn: postgres dsn
        :param max_size: максимальное количество доступных соединений
        :return: объект асинхронного движка соединений
        """

        if cls._engine is None:
            cls._engine = create_async_engine(
                str(dsn),
                pool_size=max_size,
                echo=True if app_config_.okd_stage == "DEV" else False,
                **kwargs,
            )

        return cls._engine

    def create(self, **kwargs) -> Engine | AsyncEngine:
        """
        Создать движок соединений
        :return: объект движка соединений
        """

        return self._create(self._dsn, self._max_size, **kwargs)
