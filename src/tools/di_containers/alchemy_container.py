from dependency_injector import containers, providers

from config import pg_config
from repositories import alchemy_connection_proxy
from tools.factories import alchemy_engine_factory
from uows import alchemy_uow

config = pg_config.pg_config


class AlchemyContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с БД Postgres через сессию Алхимии
    """

    wiring_config = containers.WiringConfiguration(packages=["services"])

    engine_factory = providers.Singleton(
        alchemy_engine_factory.AlchemyEngineFactory,
        config.postgres_dsn,
        config.connection_pool_size,
    )
    connection_proxy = providers.Factory(
        alchemy_connection_proxy.AlchemyConnectionProxy, engine_factory
    )

    uow = providers.Factory(alchemy_uow.AlchemyUOW, connection_proxy)
