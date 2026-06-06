from fastapi import HTTPException

from app.core.security.hashed_password import hash_password
from app.models.user_model import User
from app.repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth.user_create_schemas import UserCreate
from app.schemas.user.user import UpdateUser


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def create_user(self, user: UserCreate) -> User:
        if await self.user_repository.get_user_by_email(user.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        user.hashed_password = hash_password(user.password)
        return await self.user_repository.create_user(user)

    async def update_user(self, user_id: int, data: UpdateUser) -> User:
        user = await self.user_repository.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None and key != "id":
                setattr(user, key, value)
        return await self.user_repository.update_user(user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await self.user_repository.delete_user(user_id)

    async def get_all_users(self) -> list[User]:
        return await self.user_repository.get_all_users()

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.user_repository.get_user_by_email(email)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_repository.get_user_by_username(username)
