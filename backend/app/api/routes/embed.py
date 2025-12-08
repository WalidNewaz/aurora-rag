from fastapi import APIRouter, Depends
from app.core.container import get_container

router = APIRouter(tags=["Embed"])

@router.get("/embed")
async def embed(q: str, container = Depends(get_container)):
    embedding_provider = container.embedding_provider
    embeds = await embedding_provider.embed(q)
    return {"query": q, "results": embeds}