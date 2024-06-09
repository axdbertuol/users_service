# UserService to handle user-related operations

from typing import List


from xeez_pyutils.common import CommonQueryParams
from xeez_pyutils.exceptions import NotFoundError
from .models import User
from .protocols.service import UserServiceProtocol
from .schemas import UserCreateIn, UserUpdateIn
from .repository import UserRepository


class UserService(UserServiceProtocol):
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_item(self, body: UserCreateIn) -> User:
        user_dict = body.model_dump()
        user_dict["hashed_password"] = (
            "hash_password_function(user_create_request.password)"
        )
        del user_dict["password"]
        created_user = self.user_repo.create(User(), user_dict)
        return created_user

    def update_item(self, item_id: int, body: UserUpdateIn) -> None:
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        user_dict = body.model_dump(exclude_unset=True)
        self.user_repo.update(user, user_dict)

    def delete_item(self, item_id: int) -> None:
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        self.user_repo.delete(user)

    def fetch_item(self, item_id: int) -> User:
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        return user

    def fetch_many_items(self, q: CommonQueryParams) -> List[User]:
        return self.user_repo.get_multi(User, skip=q.skip, limit=q.limit)
