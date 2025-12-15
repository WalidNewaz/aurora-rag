import psycopg
from typing import Optional, Any

from app.core.database import Database
from app.core.logging import logger
from app.domain.models.artifact import Artifact
from app.domain.repositories.artifact_repository import ArtifactRepository


class PostgresArtifactRepository(ArtifactRepository):
    """
    Artifact repository.

    Contract:
    - Write operations REQUIRE an explicit transaction connection.
    - Repository does not manage commits or rollbacks.
    """

    def __init__(self, db: Database):
        self.db = db

    async def _fetchone(
            self,
            query: str,
            params: dict[str, Any],
            *,
            conn: psycopg.AsyncConnection | None,
    ):
        if conn is None:
            return await self.db.fetchone(query, params)

        async with conn.cursor() as cur:
            await cur.execute(query, params)
            return await cur.fetchone()

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
        query = """
            INSERT INTO artifacts (
                source_id,
                type,
                mime_type,
                path,
                size_bytes
            )
            VALUES (
                %(source_id)s,
                %(type)s,
                %(mime_type)s,
                %(path)s,
                %(size_bytes)s
            )
            RETURNING *
        """
        params = {
            "source_id": source_id,
            "type": type,
            "mime_type": mime_type,
            "path": path,
            "size_bytes": size_bytes,
        }

        row = await self._fetchone(query, params, conn=conn)
        if not row:
            raise RuntimeError("Artifact insert failed")

        logger.info("Created artifact", extra={"artifact_id": row["id"]})
        return Artifact(**row)


    async def delete(
            self,
            artifact_id: int,
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Artifact]:
        query = """
            DELETE FROM artifacts
            WHERE id = %(id)s
            RETURNING *
        """
        params = {"id": artifact_id}

        row = await self._fetchone(query, params, conn=conn)
        if row:
            logger.info("Deleted artifact", extra={"artifact_id": artifact_id})

        return Artifact(**row) if row else None