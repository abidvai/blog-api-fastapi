from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.test import test_router
from app.routers.auth_route import auth_route
from app.routers.user_router import user_router
from app.routers.blog_router import blog_router
from app.routers.like_router import like_router
from app.routers.comment_router import comment_router
from app.routers.view_router import view_router
from app.database.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(test_router, prefix="/v1")
app.include_router(auth_route, prefix="/v1")
app.include_router(user_router, prefix="/v1")
app.include_router(blog_router, prefix="/v1")
app.include_router(like_router, prefix="/v1")
app.include_router(comment_router, prefix="/v1")
app.include_router(view_router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to the Blog API!"}

