from fastapi import Request
from fastapi.responses import JSONResponse

from .responses import ErrorModel, ResponseModel


class BadValueError(ValueError):
    """Error raised for bad input values."""

    pass


class NotFoundError(Exception):
    """Error raised when a resource is not found."""

    pass


class DuplicatedError(Exception):
    """Error raised when a resource is duplicated."""

    pass


class InternalServerError(Exception):
    """Error raised for internal server errors."""

    pass


class DatabaseError(Exception):
    """Error raised for generic database errors."""

    pass


class DatabaseIntegrityError(Exception):
    """Error raised for database integrity errors."""

    pass


async def bad_value_error_exception_handler(request: Request, exc: DatabaseError):
    """Exception handler for BadValueError.

    Args:
        request (Request): The request object.
        exc (DatabaseError): The exception object.

    Returns:
        JSONResponse: JSON response containing error details.

    """

    text = "Bad Value error"
    message = text + ":" + str(exc) if str(exc) else text
    error = ErrorModel(message=message, type="BadValueErr")
    response_model: ResponseModel[None] = ResponseModel(success=False, error=error)
    return JSONResponse(status_code=400, content=response_model.model_dump())


async def database_integrity_error_exception_handler(
    request: Request, exc: DatabaseError
):
    """Exception handler for DatabaseIntegrityError.

    Args:
        request (Request): The request object.
        exc (DatabaseError): The exception object.

    Returns:
        JSONResponse: JSON response containing error details.

    """

    text = "Database Integrity error"
    message = text + ":" + str(exc) if str(exc) else text
    error = ErrorModel(message=message, type="DatabaseIntegrityErr")
    response_model: ResponseModel[None] = ResponseModel(success=False, error=error)
    return JSONResponse(status_code=400, content=response_model.model_dump())


async def database_error_exception_handler(request: Request, exc: DatabaseError):
    """Exception handler for DatabaseError.

    Args:
        request (Request): The request object.
        exc (DatabaseError): The exception object.

    Returns:
        JSONResponse: JSON response containing error details.

    """
    text = "Database error"
    message = text + ":" + str(exc) if str(exc) else text
    error = ErrorModel(message=message, type="DatabaseErr")
    response_model: ResponseModel[None] = ResponseModel(success=False, error=error)
    return JSONResponse(status_code=400, content=response_model.model_dump())


async def not_found_exception_handler(request: Request, exc: NotFoundError):
    """Exception handler for NotFoundError.

    Args:
        request (Request): The request object.
        exc (NotFoundError): The exception object.

    Returns:
        JSONResponse: JSON response containing error details.

    """
    text = "Not found"
    message = text + ":" + str(exc) if str(exc) else text
    error = ErrorModel(message=message, type="NotFound")
    response_model: ResponseModel[None] = ResponseModel(success=False, error=error)
    return JSONResponse(status_code=404, content=response_model.model_dump())


async def duplicated_exception_handler(request: Request, exc: DuplicatedError):
    """Exception handler for DuplicatedError.

    Args:
        request (Request): The request object.
        exc (DuplicatedError): The exception object.

    Returns:
        JSONResponse: JSON response containing error details.

    """
    text = "Duplicated entry"
    message = text + ":" + str(exc) if str(exc) else text
    error = ErrorModel(message=message, type="DuplicatedEntry")
    response_model: ResponseModel[None] = ResponseModel(success=False, error=error)
    return JSONResponse(status_code=400, content=response_model.model_dump())


async def internal_server_error_exception_handler(
    request: Request, exc: InternalServerError
):
    """Exception handler for InternalServerError.

    Args:
        request (Request): The request object.
        exc (InternalServerError): The exception object.

    Returns:
        JSONResponse: JSON response containing error details.

    """
    text = "Unknown error"
    message = text + ":" + str(exc) if str(exc) else text
    error = ErrorModel(message=message, type="UnknownErr")
    response_model: ResponseModel[None] = ResponseModel(success=False, error=error)
    return JSONResponse(status_code=500, content=response_model.model_dump())


exception_to_handler_list = [
    (BadValueError, bad_value_error_exception_handler),
    (NotFoundError, not_found_exception_handler),
    (DuplicatedError, duplicated_exception_handler),
    (InternalServerError, internal_server_error_exception_handler),
    (DatabaseError, database_error_exception_handler),
    (DatabaseIntegrityError, database_integrity_error_exception_handler),
]
