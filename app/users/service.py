from typing import Any, List

from aiokafka import AIOKafkaProducer
from fastapi import HTTPException, status
from pydantic import ValidationError
from xeez_pyutils.common import CommonQueryParams
from xeez_pyutils.exceptions import InternalServerError, NotFoundError

from .models import User
from .protocols.service import UserServiceProtocol
from .repository import UserRepository
from .schemas import (
    KafkaEvent,
    UserUpdateIn,
)
from .schemas import User as UserSchema


class UserService(UserServiceProtocol):
    def __init__(self, user_repo: UserRepository, aioproducer: AIOKafkaProducer):
        self.user_repo = user_repo
        self.aioproducer = aioproducer

    def get_by_username(self, username: str) -> User:
        user = self.user_repo.get_by_username(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def create_item(self, body: dict[str, Any]) -> User:
        if body.get("password"):
            del body["password"]
        created_user = self.user_repo.create(User(), body)
        return created_user

    async def update_user(self, item_id: str, body: UserUpdateIn) -> None:
        self.update_item(item_id, body)
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        try:
            payload = UserSchema.model_validate(user).model_dump()
            value = KafkaEvent(
                id=user.id.__str__(), type="user_updated", payload=payload
            ).model_dump_json()
            await self.aioproducer.send(
                topic="user-events",
                value=value.encode("utf-8"),
                key=payload["email"].encode("utf-8"),
            )
            # return user
        except ValidationError as e:
            raise InternalServerError(
                "Something went wrong during processing of event", e
            )
        except Exception as e:
            raise InternalServerError(
                "Something went wrong during kafka message sending", e
            )

    def update_item(self, item_id: str, body: UserUpdateIn) -> None:
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        user_dict = body.model_dump(exclude_unset=True)
        self.user_repo.update(user, user_dict)

    async def delete_user(self, item_id: str) -> None:
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        self.delete_item(item_id)
        email = user.email.__str__()
        try:
            payload = {"user_id": item_id}
            value = KafkaEvent(
                id=item_id, type="user_deleted", payload=payload
            ).model_dump_json()
            await self.aioproducer.send(
                topic="user-events",
                value=value.encode("utf-8"),
                key=email.encode("utf-8"),
            )
        except ValidationError as e:
            raise InternalServerError(
                "Something went wrong during processing of event", e
            )
        except Exception as e:
            raise InternalServerError(
                "Something went wrong during kafka message sending", e
            )

    def delete_item(self, item_id: str) -> None:
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        self.user_repo.delete(user)

    def fetch_item(self, item_id: str) -> User:
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        return user

    def fetch_many_items(self, q: CommonQueryParams) -> List[User]:
        return self.user_repo.get_multi(User, skip=q.skip, limit=q.limit)
