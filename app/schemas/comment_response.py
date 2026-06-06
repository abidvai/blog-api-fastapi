from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.utils.user_mini_response import UserMiniResponse


class CommentCreate(BaseModel):
    blog_id: int
    content: str

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(BaseModel):
    id: int
    content: str
    user: UserMiniResponse
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentUpdate(BaseModel):
    content: str

    model_config = ConfigDict(from_attributes=True)

