import uvicorn
from fastapi import FastAPI

from .routers.user_routes import user_router


app = FastAPI()
app.include_router(user_router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
