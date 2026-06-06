from fastapi import APIRouter
from app.core.dependency.get_db import get_db
from app.database.database import engine

test_router = APIRouter(prefix="/test", tags=["test"])


@test_router.get("/db-test")
async def db_test():
    try:
        async with engine.connect() as connection:
            return {"message": "Database connection successful"}
    except Exception as e:
        return {"message": f"Database connection failed: {str(e)}"}
