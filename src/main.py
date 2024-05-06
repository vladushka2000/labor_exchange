from fastapi import FastAPI
import uvicorn

from entrypoints import router_registrator

app = FastAPI(title="labor exchange")
router_registrator.register_routes(app)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)
