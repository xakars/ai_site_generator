from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from core.lifespan import lifespan
from frontend_api.app import frontend_app

app = FastAPI(lifespan=lifespan)


app.mount("/frontend-api", frontend_app)
app.mount("/assets", StaticFiles(directory="src/static/assets"), name="assets")
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
