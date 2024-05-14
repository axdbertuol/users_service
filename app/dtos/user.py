from pydantic import BaseModel


# Pydantic DTOs for request and response
class UserCreateRequest(BaseModel):
    email: str
    username: str
    full_name: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    status: bool
    role: str
    social_id: str
