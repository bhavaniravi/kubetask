from fastapi import FastAPI
from kubetask.api import main

app = FastAPI()


app.include_router(main.router)
