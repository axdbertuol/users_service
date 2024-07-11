from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
import jwt
from xeez_pyutils.sqlalchemy_repository import SQLAlchemyRepository

from app.auth.schemas import TokenData
from app.auth.service import AuthService
from app.auth.utils import decode_token
from app.config import get_settings
from app.database import get_db
from app.producer import get_aioproducer
from app.users.models import User
from app.users.repository import UserRepository
from app.users.service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
settings = get_settings()


async def make_user_router_deps(
    db: Annotated[Any, Depends(get_db)],
    aioproducer: Annotated[Any, Depends(get_aioproducer)],
):
    base_repo = SQLAlchemyRepository(session=db, model_type=User)
    user_repo = UserRepository(base_repo)
    user_service = UserService(user_repo=user_repo, aioproducer=aioproducer)

    return user_service


async def make_auth_router_deps(
    db: Annotated[Any, Depends(get_db)],
    aioproducer: Annotated[Any, Depends(get_aioproducer)],
):
    base_repo = SQLAlchemyRepository(session=db, model_type=User)
    user_repo = UserRepository(base_repo)
    user_service = UserService(user_repo=user_repo, aioproducer=aioproducer)
    auth_service = AuthService(user_service=user_service, aioproducer=aioproducer)
    return auth_service


async def get_token_data(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = decode_token(token)
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    return token_data
