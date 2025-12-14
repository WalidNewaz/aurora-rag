from fastapi import FastAPI

from app.core.settings import settings
from app.core.container import get_container
from app.api.routes import register_routes
from app.middleware import register_middleware

tags_metadata = [
    {
        "name": "Sites Management",
        "description": "Endpoints related to the ingestion operations.",
    },
    {
        "name": "Sources",
        "description": "Register and manage ingestion sources (websites, repositories, files, etc.).",
    },
    {
        "name": "Ingestion Control",
        "description": "Start, pause, and monitor ingestion and indexing jobs.",
    },
    {
        "name": "RAG",
        "description": "Query and retrieval endpoints for the RAG system.",
    },
    {
        "name": "Debug / Internal",
        "description": "Internal inspection endpoints (subject to removal).",
    },
]

app = FastAPI(
    title="AuroraRAG Backend",
    version="0.1.0",
    description="RAG-based search engine backend.",
    openapi_tags=tags_metadata
)

@app.on_event("startup")
async def startup():
    container = get_container()
    await container.db.connect()

@app.on_event("shutdown")
async def shutdown():
    container = get_container()
    await container.db.close()

# Register all API routes
register_routes(app)

# Register all middleware
register_middleware(app)

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.environment}