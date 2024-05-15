from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ErrorModel(BaseModel):
    message: str
    type: Optional[str] = None
    target: Optional[str] = ""


class ResponseModel(BaseModel, Generic[T]):
    success: bool
    error: Optional[ErrorModel] = None
    data: Optional[T] = None
    model_config = ConfigDict(from_attributes=True)
