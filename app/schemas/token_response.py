from datetime import datetime
from os import access
from anyio import abc
from pydantic import BaseModel, ConfigDict


class TokenResponse(BaseModel):
    user_id: int
    access_token: str
    access_token_valid_till: datetime
    refresh_token: str
    refresh_token_valid_till: datetime
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)
