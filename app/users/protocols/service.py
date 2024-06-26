from app.users.models import User
from xeez_pyutils.protocols.service_protocol import ServiceProtocol

from app.users.schemas import UserCreateIn, UserUpdateIn


class UserServiceProtocol(ServiceProtocol[User]):

    async def create_user(self, body: UserCreateIn) -> User: ...
    async def update_user(self, item_id: int, body: UserUpdateIn) -> None: ...
    async def delete_user(self, item_id: int) -> None: ...
