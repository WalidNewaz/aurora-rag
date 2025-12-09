# -------------------------------
# Routes to manage sites.
# This is part of the crawler.
# -------------------------------
from typing import List
from fastapi import APIRouter, Depends

from app.core.container import get_container
from app.api.schemas.sites import Site, SiteCreate, SiteUpdate

router = APIRouter(
    prefix="/sites",
    tags=["Sites"],
)


@router.get("", response_model=List[Site])
async def get_sites(container=Depends(get_container)):
    repository = container.site_repository
    sites = await repository.get_all()
    print(sites)
    return sites

@router.post("", response_model=Site)
async def create_site(site: SiteCreate, container=Depends(get_container)):
    repository = container.site_repository
    site = await repository.create(url=site.url)
    return site

@router.get("/{site_id}", response_model=Site)
async def get_site(site_id: str, container=Depends(get_container)):
    return {"site_id": site_id, "seed_url": "https://www.walidnewaz.com/"}

@router.put("/{site_id}", response_model=Site)
async def update_site(site: SiteUpdate, container=Depends(get_container)):
    return {"site_id": site.site_id}

@router.delete("/{site_id}", response_model=Site)
async def delete_site(site_id: str, container=Depends(get_container)):
    return {"site_id": site_id}

