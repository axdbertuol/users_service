# UserService to handle user-related operations

from ..dtos.user import UserCreateRequest, UserResponse
from ..repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user_create_request: UserCreateRequest) -> UserResponse:
        user_dict = user_create_request.model_dump()
        user_dict["hashed_password"] = (
            "hash_password_function(user_create_request.password)"
        )
        del user_dict["password"]
        created_user = self.user_repo.create(user_dict)
        return created_user
