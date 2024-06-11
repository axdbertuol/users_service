from typing import List

from aiokafka import AIOKafkaProducer
from xeez_pyutils.common import CommonQueryParams
from xeez_pyutils.exceptions import NotFoundError, InternalServerError

from .models import User
from .protocols.service import UserServiceProtocol
from .repository import UserRepository
from .schemas import KafkaEvent, UserCreateIn, UserUpdateIn
from .schemas import User as UserSchema


class UserService(UserServiceProtocol):
    def __init__(self, user_repo: UserRepository, aioproducer: AIOKafkaProducer):
        self.user_repo = user_repo
        self.aioproducer = aioproducer

    async def create_user(self, body: UserCreateIn) -> User:
        user = self.create_item(body)
        try:
            payload = UserSchema.model_validate(user).model_dump()
            payload["user_id"] = user.id
            value = KafkaEvent(
                id=payload["email"],
                type="user_created",
                payload=payload,
            ).model_dump_json()
        except Exception as e:
            raise InternalServerError(
                "Something went wrong during processing of event", e
            )

        try:
            await self.aioproducer.send(
                topic="user-events",
                value=value.encode("utf-8"),
                key=payload["email"].encode("utf-8"),
            )
            return user
        except Exception as e:
            raise InternalServerError(
                "Something went wrong during kafka message sending", e
            )

    def create_item(self, body: UserCreateIn) -> User:
        user_dict = body.model_dump()
        user_dict["hashed_password"] = (
            "hash_password_function(user_create_request.password)"
        )
        del user_dict["password"]
        created_user = self.user_repo.create(User(), user_dict)
        return created_user

    async def update_user(self, item_id: int, body: UserUpdateIn) -> None:
        self.update_item(item_id, body)
        user = self.user_repo.get(User, item_id)
        try:
            payload = UserSchema.model_validate(user).model_dump()
            payload["user_id"] = user.id
            value = KafkaEvent(
                id=user.email, type="user_updated", payload=payload
            ).model_dump_json()
        except Exception as e:
            raise InternalServerError(
                "Something went wrong during processing of event", e
            )
        try:
            await self.aioproducer.send(
                topic="user-events",
                value=value.encode("utf-8"),
                key=payload["email"].encode("utf-8"),
            )
            return user
        except Exception as e:
            raise InternalServerError(
                "Something went wrong during kafka message sending", e
            )

    def update_item(self, item_id: int, body: UserUpdateIn) -> None:
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        user_dict = body.model_dump(exclude_unset=True)
        self.user_repo.update(user, user_dict)

    async def delete_user(self, item_id: int) -> None:
        self.delete_item(item_id)
        user = self.user_repo.get(User, item_id)

        try:
            payload = {"user_id": user.id}
            value = KafkaEvent(
                id=user.email, type="user_deleted", payload=payload
            ).model_dump_json()
        except Exception as e:
            raise InternalServerError(
                "Something went wrong during processing of event", e
            )

        try:
            await self.aioproducer.send(
                topic="user-events",
                value=value.encode("utf-8"),
                key=payload["email"].encode("utf-8"),
            )
        except Exception as e:
            raise InternalServerError(
                "Something went wrong during kafka message sending", e
            )

    def delete_item(self, item_id: int) -> None:
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        self.user_repo.delete(user)

    def fetch_item(self, item_id: int) -> User:
        user = self.user_repo.get(User, item_id)
        if user is None:
            raise NotFoundError
        return user

    def fetch_many_items(self, q: CommonQueryParams) -> List[User]:
        return self.user_repo.get_multi(User, skip=q.skip, limit=q.limit)
