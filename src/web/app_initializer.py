import fastapi
from fastapi.responses import PlainTextResponse

from config import app_config
from tools import exceptions
from web.middlewares import logger_middleware
from web.tools import router_registrator

app_config = app_config.app_config

app = fastapi.FastAPI(
    title=app_config.project_name,
    version=app_config.app_version,
    debug=True if app_config.okd_stage == "DEV" else False,
    default_response_class=fastapi.responses.JSONResponse,
)

router_registrator.register_routers(app)

app.add_middleware(logger_middleware.LogRequestInfoMiddleware)
app.add_middleware(logger_middleware.SetRequestContextMiddleware)


@app.exception_handler(Exception)
async def common_exception_handler(*args, **kwargs) -> PlainTextResponse:
    """
    Универсально обработать любой тип ошибки
    :return: 500 статус
    """

    return PlainTextResponse(status_code=500)


@app.exception_handler(exceptions.InvalidTokenException)
async def invalid_token_exception_handler(*args, **kwargs) -> PlainTextResponse:
    """
    Обработать ошибку с невалидным токеном
    :return: 403 статус
    """

    return PlainTextResponse(status_code=403)


@app.exception_handler(ConnectionError)
async def connection_error_handler(*args, **kwargs) -> PlainTextResponse:
    """
    Обработать ошибку с разорванным соединением
    :return: 500 статус
    """

    return PlainTextResponse(status_code=500)


@app.exception_handler(exceptions.PermissionDeniedException)
async def permission_denied_exception_handler(*args, **kwargs) -> PlainTextResponse:
    """
    Обработать ошибку с отказом в доступе
    :return: 403 статус
    """

    return PlainTextResponse(status_code=403)
