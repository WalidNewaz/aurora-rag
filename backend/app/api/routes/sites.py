# -------------------------------
# Routes to manage sites.
# This is part of the crawler.
# -------------------------------
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.container import get_container
from app.api.schemas.sites import (
    Site as SiteSchema,
    SiteCreate as SiteCreateSchema,
    SiteUpdate as SiteUpdateSchema,
)

router = APIRouter(
    prefix="/sites",
    tags=["Sites"],
)


@router.get("/", response_model=List[SiteSchema])
async def get_sites(container=Depends(get_container)) ->List[SiteSchema]:
    repository = container.site_repository
    sites = await repository.get_all()
    return sites

@router.post(
    "/",
    response_model=SiteSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_site(
        site: SiteCreateSchema,
        container=Depends(get_container)
) -> SiteSchema:
    repository = container.site_repository
    new_site = await repository.create(url=site.url)
    return new_site

@router.get("/{site_id}", response_model=SiteSchema)
async def get_site(site_id: int, container=Depends(get_container)) -> SiteSchema:
    repository = container.site_repository
    site = await repository.get(site_id)
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    return site

@router.patch("/{site_id}", response_model=SiteSchema)
async def update_site(
        site_id: int,
        site_update: SiteUpdateSchema,
        container=Depends(get_container)
) -> SiteSchema:
    repository = container.site_repository

    update_data = site_update.model_dump(exclude_unset=True)
    updated = await repository.update(site_id, update_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Site not found or no fields provided"
        )

    return updated

@router.delete("/{site_id}", response_model=SiteSchema)
async def delete_site(site_id: int, container=Depends(get_container)) -> SiteSchema:
    repository = container.site_repository

    deleted = await repository.delete(site_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    return deleted


