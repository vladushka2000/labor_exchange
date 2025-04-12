from fastapi import FastAPI

from config import app_config
from web.entrypoints import (
    auth_entrypoint,
    job_entrypoint,
    index_entrypoint,
    responses_entrypoint,
    users_entrypoint,
)

app_config = app_config.app_config


def register_routers(app: FastAPI) -> None:
    """
    Зарегистрировать роутеры
    :param app: приложение FastAPI
    """

    app.include_router(auth_entrypoint.router, prefix=f"/api/{app_config.app_version}")
    app.include_router(job_entrypoint.router, prefix=f"/api/{app_config.app_version}")
    app.include_router(index_entrypoint.router, prefix=f"/api/{app_config.app_version}")
    app.include_router(
        responses_entrypoint.router, prefix=f"/api/{app_config.app_version}"
    )
    app.include_router(users_entrypoint.router, prefix=f"/api/{app_config.app_version}")
