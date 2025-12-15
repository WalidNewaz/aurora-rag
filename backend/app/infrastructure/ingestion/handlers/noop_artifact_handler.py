from app.domain.ingestion.artifact_handler import ArtifactHandler
from app.domain.models.artifact import Artifact
from app.core.logging import logger


class NoOpArtifactHandler(ArtifactHandler):
    """
    No-op artifact handler.

    Used as a placeholder until real parsing handlers are implemented.
    Ensures artifact ingestion does not fail at runtime.
    """

    async def enqueue(self, artifact: Artifact) -> None:
        logger.info(
            "Artifact ingestion skipped (no-op handler)",
            extra={
                "artifact_id": artifact.id,
                "mime_type": artifact.mime_type,
                "path": artifact.path,
            },
        )
