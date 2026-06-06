from fastapi import HTTPException
from app.repository.comment_repository import CommentRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.comment_model import Comment
from app.schemas.comment_response import CommentCreate


class CommentService:
    def __init__(self, db: AsyncSession):
        self.comment_repository = CommentRepository(db)

    async def create_comment(self, user_id: int, content: CommentCreate) -> Comment:
        comment = Comment(
            user_id=user_id, post_id=content.blog_id, content=content.content
        )
        return await self.comment_repository.create_comment(comment)

    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        return await self.comment_repository.get_comment_by_id(comment_id)

    async def get_comments_by_blog_id(self, blog_id: int) -> list[Comment]:
        return await self.comment_repository.get_comments_by_blog_id(blog_id)

    async def get_comments_by_user_id(self, user_id: int) -> list[Comment]:
        return await self.comment_repository.get_comments_by_user_id(user_id)

    async def update_comment(self, comment_id: int, content: str) -> Comment:
        comment = await self.comment_repository.get_comment_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        comment.content = content
        return await self.comment_repository.update_comment(comment)

    async def delete_comment(self, comment_id: int) -> None:
        comment = await self.comment_repository.get_comment_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        await self.comment_repository.delete_comment(comment_id)

    async def get_comment_count_by_blog_id(self, blog_id: int) -> int:
        return await self.comment_repository.get_comment_count_by_blog_id(blog_id)
