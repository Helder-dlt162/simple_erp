from fastapi import FastAPI
from routes.auth import login
from db import init
from db.repositories.users import add_user, get_users, delete_user
from db.repositories.user_types import add_user_type, get_user_types
import config

app = FastAPI()
app_config = config.app_config

app.include_router(login.router)

app.title = app_config["NAME"]
app.version = app_config["VERSION"]

@app.get("/")
def root():
    return {"status": "83348, ok"}

# init.init_db()
data = {"username": "HENeto", "email": "heldere@gmail.com", "password": "12345678", "user_type": 2}
# data2 = {"name": "Common"}

print(add_user(data))
# print(get_users(1))
# print(add_user_type(data2))
# print(get_user_types())
