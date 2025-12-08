from fastapi import FastAPI
from .search import router as search_router

def register_routes(app: FastAPI):
    app.include_router(search_router, prefix="/v1")