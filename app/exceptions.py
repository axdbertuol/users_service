from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.dtos.responses import ErrorModel, ResponseModel


class NotFoundError(Exception):
    pass


class DuplicatedError(Exception):
    pass


class InternalServerError(Exception):
    pass


async def not_found_exception_handler(request: Request, exc: NotFoundError):
    error = ErrorModel(message=str(exc) if str(exc) else "Not found")
    response_model = ResponseModel(success=False, error=error)
    return JSONResponse(status_code=404, content=response_model.model_dump())


async def duplicated_exception_handler(request: Request, exc: DuplicatedError):
    error = ErrorModel(message=str(exc) if str(exc) else "Duplicated entry")
    response_model = ResponseModel(success=False, error=error)
    return JSONResponse(status_code=400, content=response_model.model_dump())


async def internal_server_error_exception_handler(
    request: Request, exc: InternalServerError
):
    error = ErrorModel(message=str(exc) if str(exc) else "Unknown error")
    response_model = ResponseModel(success=False, error=error)
    return JSONResponse(status_code=500, content=response_model.model_dump())
