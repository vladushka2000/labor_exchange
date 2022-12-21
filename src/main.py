from fastapi import FastAPI
from routers import auth, user, job, response
import uvicorn

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(job.router)
app.include_router(response.router)


@app.get("/")
def hello():
    return {"message": "Hello, world!"}


if __name__ == '__main__':
    uvicorn.run("main:app", port=8080, reload=True)
