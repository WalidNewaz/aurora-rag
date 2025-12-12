# -------------------------------
# Routes to manage sites.
# This is part of the crawler.
# -------------------------------
from typing import List
from fastapi import APIRouter, Depends, HTTPException

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
    formatted_sites = [Site(
        id = site['id'],
        url = site['url'],
        name = site['name'] or "",
        start_url = site['start_url'] or "",
        allowed_domains = site['allowed_domains'],
        max_depth = site['max_depth'],
        created_at = site['created_at'],
        last_crawled_at = site['last_crawled_at'],
    ) for site in sites]
    return formatted_sites

@router.post("", response_model=Site)
async def create_site(site: SiteCreate, container=Depends(get_container)):
    repository = container.site_repository
    new_site = await repository.create(url=site.url)
    return new_site

@router.get("/{site_id}", response_model=Site)
async def get_site(site_id: str, container=Depends(get_container)):
    repository = container.site_repository
    site = await repository.get(site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")

    return Site(
        id = site.id,
        url = site.url,
        name = site.name or "",
        start_url = site.start_url or "",
        allowed_domains = site.allowed_domains,
        max_depth = site.max_depth,
        created_at = site.created_at,
        last_crawled_at = site.last_crawled_at,
    )

@router.put("/{site_id}", response_model=Site)
async def update_site(
        site_id: str,
        site_update: SiteUpdate,
        container=Depends(get_container)
):
    repository = container.site_repository

    existing = await repository.get(site_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Site not found")

    updated = await repository.update(site_id, site_update)
    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update",
        )

    return Site(
        id=updated.id,
        url=updated.url,
        name=updated.name or "",
        start_url=updated.start_url or "",
        allowed_domains=updated.allowed_domains,
        max_depth=updated.max_depth,
        created_at=updated.created_at,
        last_crawled_at=updated.last_crawled_at,
    )

@router.delete("/{site_id}", response_model=Site)
async def delete_site(site_id: str, container=Depends(get_container)):
    return {"site_id": site_id}

