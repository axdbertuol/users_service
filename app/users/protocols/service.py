from typing import Any, Protocol
from app.users.models import User

from app.users.schemas import UserCreateIn, UserUpdateIn


class UserServiceProtocol(Protocol):

    def create_item(self, body: dict[str, Any]) -> User: ...
    async def update_user(self, item_id: str, body: UserUpdateIn) -> None: ...
    async def delete_user(self, item_id: str) -> None: ...
