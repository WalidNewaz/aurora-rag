from fastapi import FastAPI
from .search import router as search_router
from .embed import router as embed_router
from .crawl import router as crawl_router

def register_routes(app: FastAPI):
    app.include_router(search_router, prefix="/v1")
    app.include_router(embed_router, prefix="/v1")
    app.include_router(crawl_router, prefix="/v1")