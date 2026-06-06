from sqlalchemy.ext.asyncio import AsyncSession
from app.models.like_model import Like
from app.repository.like_repository import LikeRepository


class LikeService:
    def __init__(self, db: AsyncSession):
        self.like_repository = LikeRepository(db)

    async def toggle_like(self, user_id: int, blog_id: int):
        existing = await self.like_repository.get_like(user_id, blog_id)

        if existing:
            await self.like_repository.delete_like(existing.id)
            return {"liked": False}
        else:
            like = Like(user_id=user_id, blog_id=blog_id)
            await self.like_repository.create_like(like)
            return {"liked": True}

    async def get_likes_by_blog_id(self, blog_id: int) -> list[Like]:
        return await self.like_repository.get_likes_by_blog_id(blog_id)

    async def get_likes(self, user_id: int) -> list[Like]:
        return await self.like_repository.get_like(user_id)
