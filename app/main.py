import os
from app.producer import lifespan
from .initiator import init_app

if os.getenv("KAFKA_STATUS") == "true":
    app = init_app(lifespan=lifespan)
else:
    app = init_app()


@app.get("/")
def read_root():
    return {"Hello": "World"}
