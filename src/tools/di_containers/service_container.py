from dependency_injector import containers, providers

from config import pg_config
from services import auth_service, jobs_service, responses_service, users_service

config = pg_config.pg_config


class ServiceContainer(containers.DeclarativeContainer):
    """
    DI-контейнер с провайдерами для работы с сервисами
    """

    wiring_config = containers.WiringConfiguration(
        modules=["web.dependencies.auth_dependency"], packages=["web.entrypoints"]
    )

    auth_service = providers.Factory(auth_service.AuthService)
    users_service = providers.Factory(users_service.UsersService)
    jobs_service = providers.Factory(jobs_service.JobsService)
    responses_service = providers.Factory(responses_service.ResponsesService)
