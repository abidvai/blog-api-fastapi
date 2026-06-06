from starlette.status import HTTP_400_BAD_REQUEST
from app.schemas.auth.user_create_schemas import UserCreate
from app.core.security.hashed_password import hash_password
from app.models.user_model import User
from datetime import datetime, timedelta, timezone
from app.core.security.hashed_password import verify_password
from app.schemas.token_response import TokenResponse
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.user_repository import UserRepository
from app.schemas.auth.login import LoginUser
from app.core.security.jwt_token import create_access_token, create_refresh_token
from app.core.settings import settings

class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def login(self, data: LoginUser):
        user = await self.user_repository.get_user_by_email(data.email)

        if not user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid Email")
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid Password")
        
        access_token_valid_till = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        refresh_token_valid_till = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )
        
        return TokenResponse(
            user_id=user.id,
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
            access_token_valid_till=access_token_valid_till,
            refresh_token_valid_till=refresh_token_valid_till,
            token_type="bearer"
        )

    async def register(self, data: UserCreate) -> TokenResponse:
        user = await self.user_repository.get_user_by_email(data.email)
        if user:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User already exists")
        
        user = User(email=data.email, hashed_password=hash_password(data.password), username=data.username, profile_picture_url=data.profile_picture_url)
        user = await self.user_repository.create_user(user)
        
        return TokenResponse(
            user_id=user.id,
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
            access_token_valid_till=datetime.now(timezone.utc) + timedelta(
                minutes=settings.access_token_expire_minutes
            ),
            refresh_token_valid_till=datetime.now(timezone.utc) + timedelta(
                days=settings.refresh_token_expire_days
            ),
            token_type="bearer"
        )    