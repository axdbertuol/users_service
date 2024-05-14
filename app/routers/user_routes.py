# Route handler
from typing import Annotated, Union
from fastapi import APIRouter, Depends

from ..dependencies import make_user_router_deps
from ..config.constants import API_PREFIX
from ..services.user_service import UserService
from ..dtos.user import UserCreateRequest, UserResponse

user_router = APIRouter(prefix=API_PREFIX)


class CommonQueryParams:
    def __init__(self, q: Union[str, None] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@user_router.post("/users/", response_model=UserResponse)
def create_user(
    user_create_request: UserCreateRequest,
    user_service: Annotated[UserService, Depends(make_user_router_deps)],
):
    return user_service.create_user(user_create_request)
