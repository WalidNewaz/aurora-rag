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
    tags=["Sites Management"],
)


@router.get("/", response_model=List[SiteSchema])
async def get_sites(container=Depends(get_container)) ->List[SiteSchema]:
    """
    Fetch all registered sites.
    """
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
    """
    Create a new site.
    """
    source_repo = container.source_repository
    site_repo = container.site_repository
    db = container.db

    try:
        async with db.transaction():
            # 1. Create a source
            source = await source_repo.create(
                type="web",
                name=site.name or site.url,
                config={
                    "start_url": site.start_url or site.url,
                    "allowed_domains": site.allowed_domains,
                    "max_depth": site.max_depth,
                },
            )

            # 2. Create a site linked to the source
            new_site = await site_repo.create(
                url=site.url,
                source_id=source.id,
                name=site.name or site.url,
                start_url=site.start_url or site.url,
                allowed_domains=site.allowed_domains,
                max_depth=site.max_depth,
            )

            return new_site

    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create site",
        ) from err

@router.get("/{site_id}", response_model=SiteSchema)
async def get_site(site_id: int, container=Depends(get_container)) -> SiteSchema:
    """
    Get a site by ID.
    """
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
    """
    Update a site by ID.
    """
    repository = container.site_repository
    db = container.db

    update_data = site_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    async with db.transaction():
        updated = await repository.update(site_id, update_data)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Site not found or no fields provided"
            )

        return updated

@router.delete("/{site_id}", response_model=SiteSchema)
async def delete_site(site_id: int, container=Depends(get_container)) -> SiteSchema:
    """
    Delete a site by ID.
    """
    source_repo = container.source_repository
    site_repo = container.site_repository

    # 1. Delete the site record
    deleted_site = await site_repo.delete(site_id)
    if not deleted_site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Site not found"
        )

    # 2. Delete the source record
    deleted_source = await source_repo.delete(deleted_site.source_id)

    return deleted_site


