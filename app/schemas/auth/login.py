from pydantic import BaseModel, Field


class LoginUser(BaseModel):
    email: str = Field(..., description="The email of the user")
    password: str = Field(..., description="The password of the user")
