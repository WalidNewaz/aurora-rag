from fastapi import APIRouter, Depends
from app.core.container import get_container

router = APIRouter()

@router.post("/crawl/{site_id}")
async def crawl_site(site_id: str, container = Depends(get_container)):
    orchestrator = container.crawl_orchestrator
    await orchestrator.crawl_site(site_id)
    return {"status": "completed", "site_id": site_id}