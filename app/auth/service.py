from typing import Any
from fastapi import HTTPException, status
import jwt
from aiokafka import AIOKafkaProducer
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError


from app.auth.utils import (
    create_jwt_tokens,
    get_password_hash,
    verify_password,
)
from app.auth.protocols.service import AuthServiceProtocol
from app.auth.schemas import TokenRefresh, TokenData
from app.config import get_settings
from app.users.models import User
from app.users.schemas import UserCreateIn
from app.users.schemas import User as UserSchema
from app.users.service import UserService


# TODO: in the future, implement auth as another microservice
class AuthService(AuthServiceProtocol):
    def __init__(
        self,
        user_service: UserService,
        aioproducer: AIOKafkaProducer,
    ):
        self.aioproducer = aioproducer
        self.user_service = user_service
        self.settings = get_settings()

    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.user_service.get_by_username(username)
        if user is None:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def login(self, credentials: OAuth2PasswordRequestForm) -> dict[str, Any]:
        user = self.authenticate_user(
            username=credentials.username, password=credentials.password
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return create_jwt_tokens(user)

    async def signup(self, user_in: UserCreateIn) -> UserSchema:
        user_dict = user_in.model_dump()
        user_dict["hashed_password"] = get_password_hash(user_in.password)
        return self.user_service.create_item(user_dict)

    async def refresh_tokens(self, token: TokenRefresh) -> dict[str, str]:
        try:
            payload = jwt.decode(
                token.refresh_token,
                self.settings.secret_key,
                algorithms=[self.settings.algorithm],
                options={"verify_exp": True},
            )
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token",
                )

            return create_jwt_tokens(TokenData(username=username))
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired",
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
