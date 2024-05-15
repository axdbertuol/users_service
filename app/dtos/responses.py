from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ErrorModel(BaseModel):
    message: str
    type: Optional[str] = None
    target: Optional[str] = ""


class ResponseModelData(BaseModel):
    data: Optional[T] = None

    class Config:
        from_attributes = True


class ResponseModel(ResponseModelData, Generic[T]):
    success: bool
    error: Optional[ErrorModel] = None
