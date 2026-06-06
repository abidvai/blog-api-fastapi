from app.database import database
from app.schemas.blog.blog import CreateBlog
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.blog_model import Blog
from app.repository.blog_repository import BlogRepository
from app.schemas.blog.blog import UpdateBlog


class BlogService:
    def __init__(self, db: AsyncSession):
        self.repository = BlogRepository(db)

    async def create_blog(self, data: CreateBlog, user_id: int) -> Blog:
        blog = Blog(
            title=data.title,
            content=data.content,
            blog_photo=data.blog_photo,
            user_id=user_id,
        )
        return await self.repository.create_blog(blog)
    
    async def get_blog_by_id(self, blog_id: int) -> Blog | None:
        blog = await self.repository.get_blog_by_id(blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        return blog

    async def get_all_blogs(self) -> list[Blog]:
        return await self.repository.get_all_blogs()

    async def update_blog(self, blog_id: int, data: UpdateBlog) -> Blog:
        blog = await self.repository.get_blog_by_id(blog_id)

        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            if value is not None and key != "id":
                setattr(blog, key, value)
        return await self.repository.update_blog(blog)

    async def delete_blog(self, blog_id: int) -> None:
        blog = await self.repository.get_blog_by_id(blog_id)
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")

        await self.repository.delete_blog(blog_id)
