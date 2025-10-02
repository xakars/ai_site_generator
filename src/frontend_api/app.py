from fastapi import FastAPI

from .sites.routes import sites_router
from .users.routes import users_router

frontend_app = FastAPI()

frontend_app.include_router(users_router)
frontend_app.include_router(sites_router)
