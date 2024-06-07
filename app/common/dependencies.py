from typing import Annotated, Any
from fastapi import Depends
from ..users.models import User
from .database import get_db
from ..users.repository import UserRepository
from ..users.service import UserService


def make_user_router_deps(
    db: Annotated[Any, Depends(get_db)],
):
    user_repo = UserRepository(session=db, model_type=User)
    user_service = UserService(user_repo=user_repo)

    return user_service
