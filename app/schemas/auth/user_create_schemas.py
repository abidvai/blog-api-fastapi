from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=50, description="The username of the user"
    )
    email: EmailStr = Field(..., description="The email of the user")
    password: str = Field(..., min_length=8, description="The password of the user")
    profile_picture_url: str | None = Field(
        None, max_length=255, description="The URL of the user's profile picture"
    )
    
    model_config = ConfigDict(from_attributes=True)


