import psycopg

from app.domain.models.source import Source
from app.domain.models.artifact import Artifact
from app.domain.ingestion.source_handler import SourceHandler

class IngestionCoordinator:
    def __init__(self, handlers: dict[str, SourceHandler]):
        self.handlers = handlers

    def _get_handler(self, source_type: str) -> SourceHandler:
        handler = self.handlers.get(source_type)
        if not handler:
            raise ValueError(f"No handler registered for source type '{source_type}'")
        return handler

    async def on_source_created(self, source: Source, *, conn: psycopg.AsyncConnection) -> None:
        await self._get_handler(source.type).on_created(source, conn=conn)

    async def on_source_updated(self, source: Source, *, conn: psycopg.AsyncConnection) -> None:
        await self._get_handler(source.type).on_updated(source, conn=conn)

    async def on_source_deleted(self, source: Source, *, conn: psycopg.AsyncConnection) -> None:
        await self._get_handler(source.type).on_deleted(source, conn=conn)

    async def on_artifact_created(self, artifact: Artifact) -> None:
        """
        Fan-out point for newly created artifacts.
        This should NOT be transactional.
        """
        handler = self._get_handler_for_artifact(artifact)
        await handler.on_artifact_created(artifact)

    def _get_handler_for_artifact(self, artifact: Artifact) -> SourceHandler:
        # source_type will be resolved by artifact → source lookup later if needed
        # for now assume artifact carries enough context
        raise NotImplementedError("Artifact → handler resolution not wired yet")
