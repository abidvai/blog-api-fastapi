from pydantic import BaseModel, ConfigDict, model_validator
from typing import Any


class UserMiniResponse(BaseModel):
    id: int
    username: str
    profile_picture_url: str | None = None
    profile_picture: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="before")
    @classmethod
    def set_profile_pictures(cls, data: Any) -> Any:
        if isinstance(data, dict):
            pic = data.get("profile_picture_url") or data.get("profile_picture")
            data["profile_picture"] = pic
            data["profile_picture_url"] = pic
        else:
            pic = getattr(data, "profile_picture_url", None)
            return {
                "id": getattr(data, "id"),
                "username": getattr(data, "username"),
                "profile_picture_url": pic,
                "profile_picture": pic
            }
        return data