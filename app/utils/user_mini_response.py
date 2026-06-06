from pydantic import BaseModel, ConfigDict


class UserMiniResponse(BaseModel):
    id: int
    username: str
    profile_picture: str | None = None

    model_config = ConfigDict(from_attributes=True)