import os
import uuid
from fastapi import UploadFile
import psycopg

from app.domain.models.artifact import Artifact
from app.domain.repositories.artifact_repository import ArtifactRepository


class ArtifactService:
    """
    Responsible for:
    - storing uploaded binaries
    - creating artifact records
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
        os.makedirs(self.upload_root, exist_ok=True)

        artifact_id = str(uuid.uuid4())
        file_path = os.path.join(self.upload_root, artifact_id)

        size = 0
        with open(file_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                f.write(chunk)

        return await self.artifact_repo.create(
            source_id=source_id,
            type="upload",
            mime_type=file.content_type or "application/octet-stream",
            path=file_path,
            size_bytes=size,
            conn=conn,
        )
