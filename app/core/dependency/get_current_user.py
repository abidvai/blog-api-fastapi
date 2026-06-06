from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.settings import settings
from app.core.dependency.get_db import get_db
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User

bearer_token = HTTPBearer()


async def get_current_user(
    credential: HTTPAuthorizationCredentials = Depends(bearer_token),
    db: AsyncSession = Depends(get_db),
):
    token = credential.credentials

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Not an access token")

    user = await db.get(User, int(payload.get("sub")))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


bearer_token_optional = HTTPBearer(auto_error=False)


async def get_current_user_optional(
    credential: HTTPAuthorizationCredentials | None = Depends(bearer_token_optional),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    if not credential:
        return None
    token = credential.credentials

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
    except JWTError:
        return None

    if payload.get("type") != "access":
        return None

    user = await db.get(User, int(payload.get("sub")))
    return user

