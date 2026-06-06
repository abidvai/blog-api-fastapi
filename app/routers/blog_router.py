from fastapi import HTTPException
from app.schemas.blog.blog import UpdateBlog
from app.core.dependency import get_current_user
from app.models.user_model import User
from app.schemas.blog.blog import BlogDetailResponse
from app.schemas.blog.blog import CreateBlog
from app.services.blog_service import BlogService
from app.core.dependency import get_db
from app.utils.common_response import APIResponse
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter

blog_router = APIRouter(prefix="/blog", tags=["Blog"])

@blog_router.post("/create", response_model=APIResponse[BlogDetailResponse])
async def create_blog(data: CreateBlog, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = BlogService(db)
   
    blog = await service.create_blog(data,current_user.id)
    return APIResponse(success=True, message="Blog created successfully", data=blog)

@blog_router.get("/", response_model=APIResponse[list[BlogDetailResponse]])
async def get_all_blogs(db: AsyncSession = Depends(get_db)):
    service = BlogService(db)

    blogs = await service.get_all_blogs()
    return APIResponse(success=True, message="Blogs fetched successfully", data=blogs)

@blog_router.get("/{blog_id}", response_model=APIResponse[BlogDetailResponse])
async def get_blog_by_id(blog_id: int, db: AsyncSession = Depends(get_db)):
    service = BlogService(db)

    blog = await service.get_blog_by_id(blog_id)
    return APIResponse(success=True, message="Blog fetched successfully", data=blog)

@blog_router.put("/{blog_id}", response_model=APIResponse[BlogDetailResponse])
async def update_blog(blog_id: int, data: UpdateBlog, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = BlogService(db)
    blog = await service.get_blog_by_id(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this blog")

    blog = await service.update_blog(blog_id, data)
    return APIResponse(success=True, message="Blog updated successfully", data=blog)

@blog_router.delete("/{blog_id}", response_model=APIResponse[None])
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = BlogService(db)
    blog = await service.get_blog_by_id(blog_id)
    
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    if current_user.id != blog.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this blog")   
    
    await service.delete_blog(blog_id)
    return APIResponse(success=True, message="Blog deleted successfully", data=None)    