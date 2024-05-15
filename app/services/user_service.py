# UserService to handle user-related operations

from typing import Optional


from app.exceptions import InternalServerError, NotFoundError
from ..repositories import schemas
from ..repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user_create_request: schemas.UserCreateRequest):
        user_dict = user_create_request.model_dump()
        user_dict["hashed_password"] = (
            "hash_password_function(user_create_request.password)"
        )
        del user_dict["password"]
        created_user = self.user_repo.create(user_dict)
        try:
            parsed_user = schemas.User.from_orm(created_user)
        except Exception:
            raise InternalServerError("Error parsing to user schema")
        return parsed_user

    def get_user(self, user_id: int) -> Optional[schemas.User]:
        user = self.user_repo.get(
            user_id,
        )
        if user is None:
            raise NotFoundError
        try:
            parsed_user = schemas.User.from_orm(user)
        except Exception:
            raise InternalServerError("Error parsing to user schema")
        return parsed_user

    def update_user(
        self, user_id: int, user_update_request: schemas.UserUpdateRequest
    ) -> None:
        user = self.user_repo.get(user_id)
        if user is None:
            raise NotFoundError
        user_dict = user_update_request.model_dump(exclude_unset=True)
        self.user_repo.update(user, user_dict)

    def delete_user(self, user_id: int) -> None:
        user = self.user_repo.get(user_id)
        if user is None:
            raise NotFoundError
        delete_op = self.user_repo.delete(user)
        return delete_op
