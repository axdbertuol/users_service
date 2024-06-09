# Create specific repository classes for each model
from typing import Any, List, Type
from app.users.models import User
from app.users.protocols.repository import UserRepositoryProtocol
from xeez_pyutils.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(UserRepositoryProtocol):
    def __init__(self, base_repo: SQLAlchemyRepository[User]):
        self.base_repo = base_repo
        self.session = self.base_repo.session
        self.model_type = self.base_repo.model_type

    def create(self, db_obj: User, obj_in: dict[str, Any]) -> User:
        return self.base_repo.create(db_obj, obj_in)

    def update(self, db_obj: User, obj_in: dict[str, Any]) -> None:
        return self.base_repo.update(db_obj, obj_in)

    def delete(self, db_obj: User) -> None:
        return self.base_repo.delete(db_obj)

    def get(self, model_type: Type[User], id: int) -> User | None:
        return self.base_repo.get(model_type, id)

    def get_multi(
        self, model_type: Type[User], skip: int = 0, limit: int = 10
    ) -> List[User]:
        return self.base_repo.get_multi(model_type, skip, limit)
