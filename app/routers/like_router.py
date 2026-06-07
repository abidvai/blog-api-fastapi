from app.schemas.like import CreateLike, LikeUserResponse, ToggleLikeResponse
from fastapi import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency.get_db import get_db
from app.utils.common_response import APIResponse
from app.services.like_service import LikeService
from app.models.user_model import User
from app.core.dependency import get_current_user


like_router = APIRouter(prefix="/like", tags=["Like"])


@like_router.post("/", response_model=APIResponse[ToggleLikeResponse])
async def create_like(data: CreateLike, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = LikeService(db)
    like = await service.toggle_like(user_id=current_user.id, blog_id=data.post_id)
    return APIResponse(success=True, message="Like toggled successfully", data=like)

@like_router.delete("/{like_id}", response_model=APIResponse[None])
async def delete_like(like_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = LikeService(db)

    like = await service.get_like_by_id(like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    if current_user.id != like.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this like")   
    
    await service.delete_like(like_id)
    return APIResponse(success=True, message="Like deleted successfully", data=None)

@like_router.get("/{blog_id}", response_model=APIResponse[list[LikeUserResponse]])
async def get_likes_by_blog_id(blog_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = LikeService(db)

    likes = await service.get_likes_by_blog_id(blog_id)
    return APIResponse(success=True, message="Likes fetched successfully", data=likes)
