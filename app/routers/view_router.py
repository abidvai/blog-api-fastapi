from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency.get_db import get_db
from app.core.dependency import get_current_user_optional
from app.models.user_model import User
from app.schemas.view_response import CreateView, ViewResponse
from app.services.view_service import ViewService
from app.utils.common_response import APIResponse

view_router = APIRouter(prefix="/view", tags=["View"])


@view_router.post("/", response_model=APIResponse[None])
async def add_view(
    data: CreateView,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    service = ViewService(db)
    client_ip = request.client.host if request.client else "unknown"
    user_id = current_user.id if current_user else None
    await service.add_view(
        user_id=user_id, blog_id=data.post_id, ip_address=client_ip
    )
    return APIResponse(success=True, message="View recorded successfully", data=None)


@view_router.get("/{blog_id}/count", response_model=APIResponse[int])
async def get_view_count(blog_id: int, db: AsyncSession = Depends(get_db)):
    service = ViewService(db)
    count = await service.get_view_count_by_blog_id(blog_id)
    return APIResponse(
        success=True, message="View count fetched successfully", data=count
    )


@view_router.get("/{blog_id}", response_model=APIResponse[list[ViewResponse]])
async def get_views_by_blog_id(blog_id: int, db: AsyncSession = Depends(get_db)):
    service = ViewService(db)
    views = await service.get_views_by_blog_id(blog_id)
    return APIResponse(
        success=True, message="Views fetched successfully", data=views
    )
