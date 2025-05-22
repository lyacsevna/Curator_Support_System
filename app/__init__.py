# Инициализация приложения
from fastapi import FastAPI
from .api.v1.api import api_router

def create_app() -> FastAPI:
    app = FastAPI(title="Student Management System", version="1.0.0")
    app.include_router(api_router, prefix="/api/v1")
    return app