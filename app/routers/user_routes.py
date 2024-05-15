# Route handler
from typing import Annotated, Union
from fastapi import APIRouter, Depends
from app.dtos.responses import ResponseModel

from ..repositories.schemas import UserUpdateRequest
from ..dependencies import make_user_router_deps
from ..config.constants import API_PREFIX
from ..services.user_service import UserService
from app.repositories import schemas


user_router = APIRouter(prefix=API_PREFIX)


class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@user_router.post(
    "/users/", response_model=ResponseModel[schemas.User], status_code=201
)
async def create_user(
    user_create_request: schemas.UserCreateRequest,
    user_service: Annotated[UserService, Depends(make_user_router_deps)],
):
    user = user_service.create_user(user_create_request)
    return ResponseModel[schemas.User](success=True, data=user)


@user_router.get("/users/{user_id}", response_model=ResponseModel[schemas.User])
async def read_user(
    user_id: int, user_service: Annotated[UserService, Depends(make_user_router_deps)]
):
    user = user_service.get_user(user_id)
    return ResponseModel[schemas.User](success=True, data=user)


@user_router.put("/users/{user_id}", response_model=None)
async def update_user(
    user_id: int,
    user_update_request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends(make_user_router_deps)],
):
    user_service.update_user(user_id, user_update_request)


@user_router.delete("/users/{user_id}", response_model=None)
async def delete_user(
    user_id: int, user_service: Annotated[UserService, Depends(make_user_router_deps)]
):
    user_service.delete_user(user_id)
