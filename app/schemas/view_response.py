from pydantic import BaseModel, ConfigDict
from app.utils.user_mini_response import UserMiniResponse


class CreateView(BaseModel):
    post_id: int


class ViewResponse(BaseModel):
    id: int
    user: UserMiniResponse | None = None

    model_config = ConfigDict(from_attributes=True)

