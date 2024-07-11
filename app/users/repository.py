from typing import Any, List, Type
from app.users.models import User
from app.users.protocols.repository import UserRepositoryProtocol
from xeez_pyutils.sqlalchemy_repository import SQLAlchemyRepository
from sqlalchemy import select


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

    def get(self, model_type: Type[User], id: str) -> User | None:
        return self.base_repo.get(model_type, id)

    def get_multi(
        self, model_type: Type[User], skip: int = 0, limit: int = 10
    ) -> List[User]:
        return self.base_repo.get_multi(model_type, skip, limit)

    def get_by_username(self, username: str) -> User:

        stmt_by_username = select(User).filter_by(username=username)
        stmt_by_email = select(User).filter_by(email=username)

        user = self.session.scalars(stmt_by_username).one()
        if user is None:
            user = self.session.scalars(stmt_by_email).one()
        return user
