# Route handler
from typing import Annotated, List

from fastapi import APIRouter, Depends
from xeez_pyutils.common import CommonQueryParams
from xeez_pyutils.responses import ResponseModel

from app.config import get_settings
from app.dependencies import make_user_router_deps

from .schemas import User as UserSchema
from .schemas import UserCreateIn, UserUpdateIn
from .service import UserService

user_router = APIRouter(prefix=get_settings().get_api_prefix())


@user_router.post("/users", response_model=ResponseModel[UserSchema], status_code=201)
async def create_user(
    user_create_request: UserCreateIn,
    user_service: Annotated[UserService, Depends(make_user_router_deps)],
):
    user = await user_service.create_user(user_create_request)
    return {"success": True, "data": user}


@user_router.get("/users/{user_id}", response_model=ResponseModel[UserSchema])
async def read_user(
    user_id: int, user_service: Annotated[UserService, Depends(make_user_router_deps)]
):
    user = user_service.fetch_item(user_id)
    return {"success": True, "data": user}


@user_router.get("/users", response_model=ResponseModel[List[UserSchema]])
async def read_many_users(
    user_service: Annotated[UserService, Depends(make_user_router_deps)],
    commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)],
):
    users = user_service.fetch_many_items(commons)
    return {"success": True, "data": users}


@user_router.put("/users/{user_id}", response_model=None)
async def update_user(
    user_id: int,
    user_update_request: UserUpdateIn,
    user_service: Annotated[UserService, Depends(make_user_router_deps)],
):
    await user_service.update_user(user_id, user_update_request)


@user_router.delete("/users/{user_id}", response_model=None)
async def delete_user(
    user_id: int, user_service: Annotated[UserService, Depends(make_user_router_deps)]
):
    await user_service.delete_user(user_id)
