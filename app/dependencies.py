from typing import Annotated, Any

from fastapi import Depends

from app.database import get_db
from xeez_pyutils.sqlalchemy_repository import SQLAlchemyRepository

from app.users.models import User
from app.users.repository import UserRepository
from app.users.service import UserService


def make_user_router_deps(
    db: Annotated[Any, Depends(get_db)],
):
    base_repo = SQLAlchemyRepository(session=db, model_type=User)
    user_repo = UserRepository(base_repo)
    user_service = UserService(user_repo=user_repo)

    return user_service
