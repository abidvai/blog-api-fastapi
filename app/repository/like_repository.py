from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.like_model import Like


class LikeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_like(self, like: Like) -> Like:
        self.db.add(like)
        await self.db.commit()
        await self.db.refresh(like)
        return like

    async def delete_like(self, like_id: int) -> None:
        like = await self.db.get(Like, like_id)
        await self.db.delete(like)
        await self.db.commit()

    async def get_like(self, user_id: int, blog_id: int) -> Like | None:
        result = await self.db.execute(
            select(Like).where(Like.user_id == user_id, Like.post_id == blog_id)
        )
        return result.scalar_one_or_none()

    async def get_likes_by_blog_id(self, blog_id: int) -> list[Like]:
        result = await self.db.execute(select(Like).where(Like.post_id == blog_id))
        return result.scalars().all()

    async def get_like_count_by_blog_id(self, blog_id: int) -> int:
        result = await self.db.execute(
            select(func.count(Like.id)).where(Like.post_id == blog_id)
        )
        return result.scalar_one_or_none() or 0

    
