from typing import Any, Self
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    ValidationInfo,
    field_validator,
    model_validator,
)


class UserBase(BaseModel):
    email: str
    username: str
    full_name: str

    @field_validator("username")
    @classmethod
    def check_alphanumeric(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            is_alphanumeric = v.replace(" ", "").isalnum()
            assert is_alphanumeric, f"{info.field_name} must be alphanumeric"
        return v

    @field_validator("full_name")
    @classmethod
    def check_alpha(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            is_alpha = v.replace(" ", "").isalpha()
            assert is_alpha, f"{info.field_name} must be alpha"
        return v


class User(UserBase):
    id: int
    status: str = "inactive"
    hashed_password: str | None = None
    role: str = "user"
    social_id: str | None = None

    @model_validator(mode="after")
    def check_password_social_id(self) -> Self:
        if self.hashed_password is None and self.social_id is None:
            raise ValueError("either password or social_id must be specified")
        return self

    model_config = ConfigDict(from_attributes=True)


class UserUpdateIn(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreateSocialIn(UserBase):
    social_id: str | None = None


class UserCreateIn(UserBase):
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreatePayload(BaseModel):
    user_id: int
    email: EmailStr
    username: str
    hashed_password: str
    social_id: str
    role: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class UserUpdatePayload(BaseModel):
    user_id: int
    email: EmailStr | None = None
    username: str | None = None
    hashed_password: str | None = None
    social_id: str | None = None
    role: str | None = None
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)


class KafkaEvent(BaseModel):
    id: str
    type: str
    payload: dict[str, Any]
