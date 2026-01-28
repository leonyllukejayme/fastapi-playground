from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user, auth

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"➡️ Request: {request.method} {request.url}")

    response = await call_next(request)

    print(f"⬅️ Response status: {response.status_code}")

    return response