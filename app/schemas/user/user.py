from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    profile_picture_url: str | None = None
    bio: str | None = None
    created_at: datetime
    password_updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    profile_picture_url: str | None = None
    bio: str | None = None

    model_config = ConfigDict(from_attributes=True)
