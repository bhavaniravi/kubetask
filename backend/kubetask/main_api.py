from fastapi import FastAPI
from kubetask.api import main

app = FastAPI()


app.include_router(main.job_router)
app.include_router(main.ns_router)
