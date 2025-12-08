from fastapi import APIRouter, Depends
from app.core.container import get_container

router = APIRouter()

@router.get("/search")
async def search(q: str, container = Depends(get_container)):
    retriever = container.retriever
    chunks = await retriever.retrieve(q)
    return {"query": q, "results": [c.text for c in chunks]}

