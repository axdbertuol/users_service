# Route handler
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from xeez_pyutils.responses import ResponseModel

from app.auth.schemas import Token, TokenData, TokenRefresh
from app.auth.service import AuthService
from app.config import get_settings
from app.dependencies import (
    get_token_data,
    make_auth_router_deps,
)
from app.users.schemas import User as UserSchema
from app.users.schemas import UserCreateIn

auth_router = APIRouter(prefix=get_settings().get_api_prefix())


@auth_router.post(
    "/auth/signup", response_model=ResponseModel[UserSchema], status_code=201
)
async def signup(
    user_in: UserCreateIn,
    auth_service: Annotated[AuthService, Depends(make_auth_router_deps)],
):
    user = await auth_service.signup(user_in)
    return {"success": True, "data": user}


@auth_router.post("/auth/login", response_model=Token, status_code=200)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(make_auth_router_deps)],
):
    tokens = await auth_service.login(form_data)
    return tokens


@auth_router.post("/auth/refresh_tokens", response_model=Token, status_code=200)
async def refresh_tokens(
    token_refresh: TokenRefresh,
    token_data: Annotated[TokenData, Depends(get_token_data)],
    auth_service: Annotated[AuthService, Depends(make_auth_router_deps)],
):
    tokens = await auth_service.refresh_tokens(token_refresh)
    return tokens
