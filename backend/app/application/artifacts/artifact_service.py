import os
import uuid
from pathlib import Path

from fastapi import UploadFile
import psycopg

from app.domain.models.artifact import Artifact
from app.domain.repositories.artifact_repository import ArtifactRepository


class ArtifactService:
    """
    ArtifactService

    Responsibilities:
    - Persist uploaded binary files to disk
    - Create artifact records in the database

    Non-responsibilities:
    - Parsing artifacts
    - Chunking
    - Embedding
    - Dispatching ingestion

    IMPORTANT:
    - All methods assume they are called inside an existing DB transaction.
    """

    def __init__(
        self,
        *,
        artifact_repo: ArtifactRepository,
        upload_root: str,
    ):
        self.artifact_repo = artifact_repo
        self.upload_root = upload_root

    async def store_upload(
        self,
        *,
        source_id: int,
        file: UploadFile,
        conn: psycopg.AsyncConnection,
    ) -> Artifact:
        """
        Store an uploaded file and create an artifact record.

        This method is transactional:
        - If DB insert fails → file is deleted
        - If file write fails → no DB record is created
        """
        os.makedirs(self.upload_root, exist_ok=True)
        source_dir = Path(self.upload_root) / f"source_{source_id}"
        source_dir.mkdir(parents=True, exist_ok=True)

        suffix = Path(file.filename or "").suffix
        artifact_id = f"{uuid.uuid4()}{suffix}"
        file_path = source_dir / artifact_id

        try:
            size = 0
            with open(file_path, "wb") as f:
                while chunk := await file.read(1024 * 1024):
                    size += len(chunk)
                    f.write(chunk)

            return await self.artifact_repo.create(
                source_id=source_id,
                type="upload",
                mime_type=file.content_type or "application/octet-stream",
                path=str(file_path),
                size_bytes=size,
                conn=conn,
            )

        except Exception:
            if file_path.exists():
                file_path.unlink()
            raise

    async def remove_upload(
            self,
            artifact: Artifact,
            *,
            conn: psycopg.AsyncConnection
    ) -> None:
        """
        Remove artifact file and DB record.

        Must be called inside a transaction.
        """
        path = Path(artifact.path)
        if path.exists():
            path.unlink()
        await self.artifact_repo.delete(artifact.id, conn=conn)


