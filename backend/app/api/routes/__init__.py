from fastapi import FastAPI
from .search import router as search_router
from .embed import router as embed_router
from .crawl import router as crawl_router
from .sites import router as sites_router
from .sources import router as sources_router

def register_routes(app: FastAPI):
    app.include_router(search_router, prefix="/v1")
    app.include_router(embed_router, prefix="/v1")
    app.include_router(crawl_router, prefix="/v1")
    app.include_router(sites_router, prefix="/v1")
    app.include_router(sources_router, prefix="/v1")