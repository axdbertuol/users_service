import os
import uvicorn
from fastapi import FastAPI

from app.common.exceptions import (
    InternalServerError,
    NotFoundError,
    DuplicatedError,
    duplicated_exception_handler,
    internal_server_error_exception_handler,
    not_found_exception_handler,
)

from .users.user_routes import user_router

app = FastAPI(debug=True)
app.include_router(user_router)


app.add_exception_handler(NotFoundError, not_found_exception_handler)
app.add_exception_handler(DuplicatedError, duplicated_exception_handler)
app.add_exception_handler(InternalServerError, internal_server_error_exception_handler)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    port = os.getenv("APP_PORT", 8000)
    uvicorn.run(app, host="0.0.0.0", port=int(port))
