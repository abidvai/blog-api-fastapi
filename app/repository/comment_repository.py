from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from app.models.comment_model import Comment


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_comment(self, comment: Comment) -> Comment:
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        # Load user relation specifically for serialization
        result = await self.db.execute(
            select(Comment).where(Comment.id == comment.id).options(selectinload(Comment.user))
        )
        return result.scalar_one()

    async def update_comment(self, comment: Comment) -> Comment:
        await self.db.commit()
        await self.db.refresh(comment)
        # Load user relation specifically for serialization after update
        result = await self.db.execute(
            select(Comment).where(Comment.id == comment.id).options(selectinload(Comment.user))
        )
        return result.scalar_one()

    async def delete_comment(self, comment_id: int) -> None:
        comment = await self.db.get(Comment, comment_id)
        await self.db.delete(comment)
        await self.db.commit()

    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        result = await self.db.execute(
            select(Comment).where(Comment.id == comment_id).options(selectinload(Comment.user))
        )
        return result.scalar_one_or_none()

    async def get_comments_by_blog_id(self, blog_id: int) -> list[Comment]:
        result = await self.db.execute(
            select(Comment).where(Comment.post_id == blog_id).options(selectinload(Comment.user))
        )
        return result.scalars().all()

    async def get_comments_by_user_id(self, user_id: int) -> list[Comment]:
        result = await self.db.execute(
            select(Comment).where(Comment.user_id == user_id).options(selectinload(Comment.user))
        )
        return result.scalars().all()

    async def get_comment_count_by_blog_id(self, blog_id: int) -> int:
        result = await self.db.execute(
            select(func.count(Comment.id)).where(Comment.post_id == blog_id)
        )
        return result.scalar_one_or_none() or 0
