from typing import Any, Protocol
from app.users.models import User
from xeez_pyutils.protocols.service_protocol import ServiceProtocol

from app.users.schemas import UserCreateIn, UserUpdateIn, User as UserSchema
from app.auth.schemas import TokenRefresh, UserLogin, Token


class AuthServiceProtocol(Protocol):

    async def login(self, credentials: UserLogin) -> Token: ...
    async def signup(self, user_in: UserCreateIn) -> UserSchema: ...
    async def refresh_tokens(self, token: TokenRefresh) -> Token: ...
