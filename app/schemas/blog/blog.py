from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.utils.user_mini_response import UserMiniResponse


class CreateBlog(BaseModel):
    title: str = Field(
        ..., min_length=3, max_length=100, description="The title of the blog"
    )
    content: str = Field(..., min_length=10, description="The content of the blog")

    model_config = ConfigDict(from_attributes=True)


class UpdateBlog(BaseModel):
    title: str | None = Field(
        None, min_length=3, max_length=100, description="The title of the blog"
    )
    content: str | None = Field(
        None, min_length=10, description="The content of the blog"
    )

    model_config = ConfigDict(from_attributes=True)


class BlogBaseResponse(BaseModel):
    id: int
    title: str
    content: str
    user: UserMiniResponse

    model_config = ConfigDict(from_attributes=True)


class BlogDetailResponse(BlogBaseResponse):
    likes_count: int
    comments_count: int
    views_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
