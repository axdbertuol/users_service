from .initiator import init_app


app = init_app()


@app.get("/")
def read_root():
    return {"Hello": "World"}
