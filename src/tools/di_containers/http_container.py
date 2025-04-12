from dependency_injector import containers, providers

from repositories import http_connection_proxy, http_repository
from uows import http_uow


class HTTPIntegrationContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами HTTP-интеграции
    """

    wiring_config = containers.WiringConfiguration(packages=["services"])

    http_session = providers.Factory(http_connection_proxy.HTTPSession)
    http_repository = providers.Factory(http_repository.HTTPRepository, http_session)
    http_async_uow = providers.Factory(http_uow.HTTPUOW, http_repository)
