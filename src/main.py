from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apps.sites.app import app_sites
from apps.users.app import app_users
from core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)


app.mount("/sites", app_sites)
app.mount("/users", app_users)
app.mount("/assets", StaticFiles(directory="src/static/assets"), name="assets")
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
