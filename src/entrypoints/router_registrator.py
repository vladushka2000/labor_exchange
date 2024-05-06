from fastapi import FastAPI

from . import auth_router, job_router, main_router, response_router, user_router


def register_routes(app: FastAPI) -> None:
    app.include_router(main_router)
    app.include_router(auth_router)
    app.include_router(job_router)
    app.include_router(user_router)
    app.include_router(response_router)
