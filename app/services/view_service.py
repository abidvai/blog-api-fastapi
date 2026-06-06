from app.repository.view_repository import ViewRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.view_post_model import ViewPost as View


class ViewService:
    def __init__(self, db: AsyncSession):
        self.view_repository = ViewRepository(db)

    async def add_view(self, user_id: int | None, blog_id: int, ip_address: str):
        already_viewed = await self.view_repository.has_viewed(
            user_id, blog_id, ip_address
        )
        if not already_viewed:
            view = View(user_id=user_id, post_id=blog_id, ip_address=ip_address)
            await self.view_repository.create_view(view)
        return None

    async def get_views_by_blog_id(self, blog_id: int) -> list[View]:
        return await self.view_repository.get_views_by_blog_id(blog_id)

    async def get_views_by_user_id(self, user_id: int) -> list[View]:
        return await self.view_repository.get_views_by_user_id(user_id)

    async def has_viewed(self, user_id: int | None, blog_id: int, ip_address: str) -> bool:
        return await self.view_repository.has_viewed(user_id, blog_id, ip_address)

    async def get_view_count_by_blog_id(self, blog_id: int) -> int:
        return await self.view_repository.get_view_count_by_blog_id(blog_id)
