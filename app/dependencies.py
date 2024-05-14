from typing import Annotated, Any
from fastapi import Depends
from .repositories.models import User
from .repositories.database import get_db
from .repositories.user_repository import UserRepository
from .services.user_service import UserService


def make_user_router_deps(
    db: Annotated[Any, Depends(get_db)],
):
    user_repo = UserRepository(session=db, model_type=User)
    user_service = UserService(user_repo=user_repo)

    return user_service
