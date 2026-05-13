from fastapi import FastAPI
from routes.auth import login
from db import init
import config

app = FastAPI()
app_config = config.app_config

app.include_router(login.router)

app.title = app_config["NAME"]
app.version = app_config["VERSION"]

@app.get("/")
def root():
    return {"status": "83348, ok"}

init.init_db()