from pydantic import BaseModel, ConfigDict

from app.utils.user_mini_response import UserMiniResponse
from pydantic import BaseModel


class CreateLike(BaseModel):
    post_id: int

    model_config = ConfigDict(from_attributes=True)


class LikeUserResponse(BaseModel):
    id: int
    post_id: int
    user: UserMiniResponse

    model_config = ConfigDict(from_attributes=True)
