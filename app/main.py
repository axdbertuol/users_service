from app.producer import lifespan
from .initiator import init_app


app = init_app(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}
