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
    status: bool

    class Config:
        orm_mode = True