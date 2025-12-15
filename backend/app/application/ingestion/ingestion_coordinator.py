import psycopg

from app.domain.models.source import Source
from app.domain.models.artifact import Artifact
from app.domain.ingestion.source_handler import SourceHandler
from app.domain.ingestion.artifact_handler import ArtifactHandler


class IngestionCoordinator:
    """
    Coordinates ingestion lifecycle events.

    Rules:
    - Source handlers run INSIDE transactions
    - Artifact handlers run OUTSIDE transactions
    - Coordinator does NOT perform ingestion itself
    """

    def __init__(
            self,
            source_handlers: dict[str, SourceHandler],
            artifact_handlers: dict[str, ArtifactHandler],
    ) -> None:
        self.source_handlers = source_handlers
        self.artifact_handlers = artifact_handlers

    # -----------------------------
    # Handler resolution
    # -----------------------------

    def _get_source_handler(self, source_type: str) -> SourceHandler:
        handler = self.source_handlers.get(source_type)
        if not handler:
            raise ValueError(f"No handler registered for source type '{source_type}'")
        return handler

    def _get_artifact_handler(self, artifact: Artifact) -> ArtifactHandler:
        handler = (
            self.artifact_handlers.get(artifact.mime_type)
            or self.artifact_handlers.get("*")
        )
        if not handler:
            raise ValueError(
                f"No artifact handler for mime type '{artifact.mime_type}'"
            )
        return handler

    # -----------------------------
    # Source lifecycle (transactional)
    # -----------------------------

    async def on_source_created(self, source: Source, *, conn: psycopg.AsyncConnection) -> None:
        await self._get_source_handler(source.type).on_created(source, conn=conn)

    async def on_source_updated(self, source: Source, *, conn: psycopg.AsyncConnection) -> None:
        await self._get_source_handler(source.type).on_updated(source, conn=conn)

    async def on_source_deleted(self, source: Source, *, conn: psycopg.AsyncConnection) -> None:
        await self._get_source_handler(source.type).on_deleted(source, conn=conn)

    # -----------------------------
    # Artifact lifecycle (async)
    # -----------------------------

    async def on_artifact_created(self, artifact: Artifact) -> None:
        """
        Schedule artifact for ingestion.

        This method MUST NOT:
        - modify DB state transactionally
        - block API responses
        """
        handler = self._get_artifact_handler(artifact)
        await handler.enqueue(artifact)


