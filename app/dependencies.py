from typing import Annotated, Any

from fastapi import Depends
from xeez_pyutils.sqlalchemy_repository import SQLAlchemyRepository

from app.database import get_db
from app.producer import get_aioproducer
from app.users.models import User
from app.users.repository import UserRepository
from app.users.service import UserService


def make_user_router_deps(
    db: Annotated[Any, Depends(get_db)],
    aioproducer: Annotated[Any, Depends(get_aioproducer)],
):
    base_repo = SQLAlchemyRepository(session=db, model_type=User)
    user_repo = UserRepository(base_repo)
    user_service = UserService(user_repo=user_repo, aioproducer=aioproducer)

    return user_service
