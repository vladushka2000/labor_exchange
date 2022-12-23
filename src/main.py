from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from routers import auth, user, job, response
import uvicorn

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(job.router)
app.include_router(response.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"Ошибка валидации входных данных": str(exc)}),
    )


@app.get("/")
def hello():
    return {"message": "Hello, world!"}


if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)
