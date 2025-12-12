from fastapi import FastAPI

from app.core.settings import settings
from app.api.routes import register_routes
from app.middleware import register_middleware

app = FastAPI(
    title="AuroraRAG Backend",
    version="0.1.0",
    description="RAG-based search engine backend."
)

# Register all API routes
register_routes(app)

# Register all middleware
register_middleware(app)

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.environment}