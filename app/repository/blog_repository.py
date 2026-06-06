from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.blog_model import Blog


class BlogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_blog(self, blog: Blog) -> Blog:
        self.db.add(blog)
        await self.db.commit()
        # Refresh to populate relationships or use selectinload
        await self.db.refresh(blog)
        # Load user relation specifically for serialization
        result = await self.db.execute(
            select(Blog).where(Blog.id == blog.id).options(
                selectinload(Blog.likes),
                selectinload(Blog.comments),
                selectinload(Blog.view_posts),
                selectinload(Blog.user)
            )
        )
        return result.scalar_one()

    async def update_blog(self, blog: Blog) -> Blog:
        await self.db.commit()
        await self.db.refresh(blog)
        return blog

    async def delete_blog(self, blog_id: int) -> None:
        blog = await self.db.get(Blog, blog_id)
        await self.db.delete(blog)
        await self.db.commit()

    async def get_all_blogs(self) -> list[Blog]:
        result = await self.db.execute(
            select(Blog).options(
                selectinload(Blog.likes),
                selectinload(Blog.comments),
                selectinload(Blog.view_posts),
                selectinload(Blog.user)
            )
        )
        return result.scalars().all()

    async def get_blog_by_id(self, blog_id: int) -> Blog | None:
        result = await self.db.execute(
            select(Blog).where(Blog.id == blog_id).options(
                selectinload(Blog.likes),
                selectinload(Blog.comments),
                selectinload(Blog.view_posts),
                selectinload(Blog.user)
            )
        )
        return result.scalar_one_or_none()


    async def get_blogs_by_user_id(self, user_id: int) -> list[Blog]:
        result = await self.db.execute(
            select(Blog).where(Blog.user_id == user_id).options(
                selectinload(Blog.likes),
                selectinload(Blog.comments),
                selectinload(Blog.view_posts),
                selectinload(Blog.user)
            )
        )
        return result.scalars().all()
