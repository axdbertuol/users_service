from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    hashed_password: str
    role: str = "user"
    social_id: str = ""


class User(UserBase):
    id: int
    status: str = "inactive"

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    email: Optional[str]
    username: Optional[str]
    full_name: Optional[str]

    class Config:
        from_attributes = True


class UserCreateRequest(BaseModel):
    email: str
    username: str
    full_name: str
    password: str

    class Config:
        from_attributes = True
