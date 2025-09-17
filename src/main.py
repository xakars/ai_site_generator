from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/assets", StaticFiles(directory="src/static/assets"), name="assets")

app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
