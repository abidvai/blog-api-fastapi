import email
from unittest import result

from sqlalchemy import select
from fastapi import Depends
from app.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency.get_db import get_db


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user: User) -> User:
        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int) -> None:
        user = await self.db.get(User, user_id)

        await self.db.delete(user)
        await self.db.commit()

    async def get_all_users(self) -> list[User]:
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
