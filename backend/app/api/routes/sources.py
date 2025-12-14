# -------------------------------
# Routes to manage sources.
# This is part of the ingestion pipeline.
# -------------------------------
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.container import get_container
from app.api.schemas.sources import (
    SourceSchema,
    SourceCreateSchema,
    SourceUpdateSchema,
)


router = APIRouter(
    prefix="/sources",
    tags=["Sources"],
)

@router.post("/", response_model=SourceSchema, status_code=201)
async def create_source(
    payload: SourceCreateSchema,
    container=Depends(get_container),
):
    """
    Register a new ingestion source.
    """
    source_repo = container.source_repository
    coordinator = container.ingestion_coordinator
    db = container.db

    async with db.transaction() as conn:
        source = await source_repo.create(
            type=payload.config.type,
            name=payload.name,
            config=payload.config.model_dump(),
            conn=conn,
        )

        await coordinator.on_source_created(source, conn=conn)

    return source

@router.get("", response_model=List[SourceSchema])
async def list_sources(container=Depends(get_container)) -> List[SourceSchema]:
    """
    List all registered sources.
    """
    source_repo = container.source_repository
    db = container.db

    async with db.transaction() as conn:
        sources = await source_repo.get_all(conn=conn)

        return [
            SourceSchema.model_validate(
                {
                    "id": source.id,
                    "type": source.type,
                    "name": source.name,
                    "config": source.config,  # ← contains "type"
                    "created_at": source.created_at,
                }
            )
            for source in sources
        ]

@router.get("/{source_id}", response_model=SourceSchema)
async def get_source(
    source_id: int,
    container=Depends(get_container),
) -> SourceSchema:
    source_repo = container.source_repository
    db = container.db

    async with db.transaction() as conn:
        source = await source_repo.get(source_id, conn=conn)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")

        return source

@router.patch("/{source_id}", response_model=SourceSchema)
async def update_source(
    source_id: int,
    payload: SourceUpdateSchema,
    container=Depends(get_container),
) -> SourceSchema:
    """
    Update source metadata or configuration.
    """
    source_repo = container.source_repository
    coordinator = container.ingestion_coordinator
    db = container.db

    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )

    async with db.transaction() as conn:
        source = await source_repo.get(source_id, conn=conn)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")

        if payload.config is not None:
            # Validate config against existing source.type
            if payload.config['type'] != source.type:
                raise HTTPException(
                    status_code=400,
                    detail="Source type is immutable",
                )
            update_data["config"] = payload.config

        updated = await source_repo.update(source_id, update_data, conn=conn)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Site not found or no fields provided"
            )

        await coordinator.on_source_updated(updated, conn=conn)

    return updated

