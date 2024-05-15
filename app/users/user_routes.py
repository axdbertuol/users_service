# Route handler
from typing import Annotated, Union

from fastapi import Depends

from app.common.responses import ResponseModel

from ..common.dependencies import make_user_router_deps
from .schemas import User, UserCreateRequest, UserUpdateRequest
from .user_service import UserService
from fastapi import APIRouter

from ..common.config import settings


user_router = APIRouter(prefix=settings.get_api_prefix())


class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@user_router.post("/users/", response_model=ResponseModel[User], status_code=201)
def create_user(
    user_create_request: UserCreateRequest,
    user_service: Annotated[UserService, Depends(make_user_router_deps)],
):
    user = user_service.create_user(user_create_request)
    return ResponseModel[User](success=True, data=user)


@user_router.get("/users/{user_id}", response_model=ResponseModel[User])
def read_user(
    user_id: int, user_service: Annotated[UserService, Depends(make_user_router_deps)]
):
    user = user_service.get_user(user_id)
    return ResponseModel[User](success=True, data=user)


@user_router.put("/users/{user_id}", response_model=None)
def update_user(
    user_id: int,
    user_update_request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends(make_user_router_deps)],
):
    user_service.update_user(user_id, user_update_request)


@user_router.delete("/users/{user_id}", response_model=None)
def delete_user(
    user_id: int, user_service: Annotated[UserService, Depends(make_user_router_deps)]
):
    user_service.delete_user(user_id)
