from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.models.comment_model import Comment


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_comment(self, comment: Comment) -> Comment:
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def update_comment(self, comment: Comment) -> Comment:
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def delete_comment(self, comment_id: int) -> None:
        comment = await self.db.get(Comment, comment_id)
        await self.db.delete(comment)
        await self.db.commit()

    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        return await self.db.get(Comment, comment_id)

    async def get_comments_by_blog_id(self, blog_id: int) -> list[Comment]:
        result = await self.db.execute(
            select(Comment).where(Comment.post_id == blog_id)
        )
        return result.scalars().all()

    async def get_comments_by_user_id(self, user_id: int) -> list[Comment]:
        result = await self.db.execute(
            select(Comment).where(Comment.user_id == user_id)
        )
        return result.scalars().all()

    async def get_comment_count_by_blog_id(self, blog_id: int) -> int:
        result = await self.db.execute(
            select(func.count(Comment.id)).where(Comment.post_id == blog_id)
        )
        return result.scalar_one_or_none() or 0
