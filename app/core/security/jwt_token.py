from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.settings import settings


def create_access_token(user_id: int, expires_delta: int | None = None) -> str:
    if expires_delta is None:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    payload = {"sub": str(user_id), "type": "access", "exp": expire}

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(user_id: int, expires_delta: int | None = None) -> str:
    if expires_delta is None:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=expires_delta)
    payload = {"sub": str(user_id), "type": "refresh", "exp": expire}

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
