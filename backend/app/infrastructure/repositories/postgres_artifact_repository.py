import psycopg
from app.domain.models.artifact import Artifact
from app.domain.repositories.artifact_repository import ArtifactRepository


class PostgresArtifactRepository(ArtifactRepository):

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
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO artifacts (source_id, type, mime_type, path, size_bytes)
                VALUES (%(source_id)s, %(type)s, %(mime_type)s, %(path)s, %(size_bytes)s)
                RETURNING *
                """,
                {
                    "source_id": source_id,
                    "type": type,
                    "mime_type": mime_type,
                    "path": path,
                    "size_bytes": size_bytes,
                },
            )
            row = await cur.fetchone()
            return Artifact(**row)
