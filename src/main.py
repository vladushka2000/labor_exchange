import uvicorn

from config import app_config, uvicorn_config
from tools.di_containers import alchemy_container, http_container, service_container
from web import app_initializer

app_config = app_config.app_config

service_di = service_container.ServiceContainer()
alchemy_di = alchemy_container.AlchemyContainer()
http_di = http_container.HTTPIntegrationContainer()

app = app_initializer.app


if __name__ == "__main__":
    uvicorn.run("main:app", **uvicorn_config.uvicorn_config)
