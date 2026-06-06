from app.services.comment_service import CommentService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency.get_db import get_db
from app.core.dependency import get_current_user
from app.models.user_model import User
from app.schemas.comment_response import CommentCreate, CommentResponse, CommentUpdate
from app.utils.common_response import APIResponse

comment_router = APIRouter(prefix="/comment", tags=["Comment"])


@comment_router.post("/", response_model=APIResponse[CommentResponse])
async def create_comment(
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CommentService(db)
    comment = await service.create_comment(user_id=current_user.id, content=data)
    return APIResponse(
        success=True, message="Comment created successfully", data=comment
    )


@comment_router.put("/{comment_id}", response_model=APIResponse[CommentResponse])
async def update_comment(
    comment_id: int,
    data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CommentService(db)
    comment = await service.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to update this comment"
        )
    updated_comment = await service.update_comment(comment_id, data.content)
    return APIResponse(
        success=True, message="Comment updated successfully", data=updated_comment
    )


@comment_router.delete("/{comment_id}", response_model=APIResponse[None])
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = CommentService(db)
    comment = await service.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to delete this comment"
        )
    await service.delete_comment(comment_id)
    return APIResponse(
        success=True, message="Comment deleted successfully", data=None
    )


@comment_router.get("/{blog_id}", response_model=APIResponse[list[CommentResponse]])
async def get_comments_by_blog_id(
    blog_id: int, db: AsyncSession = Depends(get_db)
):
    service = CommentService(db)
    comments = await service.get_comments_by_blog_id(blog_id)
    return APIResponse(
        success=True, message="Comments fetched successfully", data=comments
    )
