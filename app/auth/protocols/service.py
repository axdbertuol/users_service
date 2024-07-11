from typing import Any, Protocol
from fastapi.security import OAuth2PasswordRequestForm

from app.users.schemas import UserCreateIn, User as UserSchema
from app.auth.schemas import TokenRefresh


class AuthServiceProtocol(Protocol):

    async def login(self, credentials: OAuth2PasswordRequestForm) -> dict[str, Any]: ...
    async def signup(self, user_in: UserCreateIn) -> UserSchema: ...
    async def refresh_tokens(self, token: TokenRefresh) -> dict[str, str]: ...
