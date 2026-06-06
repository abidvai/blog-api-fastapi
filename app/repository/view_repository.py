from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.view_post_model import ViewPost as View


class ViewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_view(self, view: View) -> View:
        self.db.add(view)
        await self.db.commit()
        await self.db.refresh(view)
        return view

    async def delete_view(self, view_id: int) -> None:
        view = await self.db.get(View, view_id)
        await self.db.delete(view)
        await self.db.commit()

    async def get_view_by_id(self, view_id: int) -> View | None:
        return await self.db.get(View, view_id)

    async def get_views_by_blog_id(self, blog_id: int) -> list[View]:
        result = await self.db.execute(select(View).where(View.post_id == blog_id))
        return result.scalars().all()

    async def get_views_by_user_id(self, user_id: int) -> list[View]:
        result = await self.db.execute(select(View).where(View.user_id == user_id))
        return result.scalars().all()

    async def get_view_count_by_blog_id(self, blog_id: int) -> int:
        result = await self.db.execute(
            select(func.count(View.id)).where(View.post_id == blog_id)
        )
        return result.scalar_one_or_none() or 0

    async def has_viewed(
        self, user_id: int | None, blog_id: int, ip_address: str
    ) -> bool:
        if user_id is not None:
            result = await self.db.execute(
                select(View).where(View.user_id == user_id, View.post_id == blog_id)
            )
        else:
            result = await self.db.execute(
                select(View).where(
                    View.ip_address == ip_address, View.post_id == blog_id
                )
            )
        return bool(result.scalar_one_or_none())
