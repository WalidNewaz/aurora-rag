from abc import ABC, abstractmethod
from typing import Optional
import psycopg

from app.domain.models.artifact import Artifact


class ArtifactRepository(ABC):

    @abstractmethod
    async def create(
        self,
        *,
        source_id: int,
        type: str,
        mime_type: str,
        path: str,
        size_bytes: int,
        conn: psycopg.AsyncConnection,
    ) -> Artifact:
        ...

    @abstractmethod
    async def delete(
            self,
            artifact_id: int,
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Artifact]:
        ...