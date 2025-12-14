from typing import Optional
from psycopg.types.json import Json

from app.domain.repositories.source_repository import SourceRepository
from app.domain.models.source import Source
from app.core.database import Database
from app.core.logging import logger


class PostgresSourceRepository(SourceRepository):
    def __init__(self, db: Database):
        self.db = db

    async def create(
        self,
        *,
        type: str,
        name: str | None,
        config: dict,
    ) -> Source:
        row = await self.db.fetchone(
            """
            INSERT INTO sources (type, name, config)
            VALUES (%(type)s, %(name)s, %(config)s)
            RETURNING *
            """,
            {
                "type": type,
                "name": name,
                "config": Json(config),
            },
        )
        return Source(**row)

    async def get(self, source_id: int) -> Optional[Source]:
        row = await self.db.fetchone(
            "SELECT * FROM sources WHERE id = %(id)s",
            {"id": source_id},
        )
        return Source(**row) if row else None

    async def delete(self, source_id: int) -> Optional[Source]:
        row = await self.db.fetchone(
            """
            DELETE FROM sources
            WHERE id = %(id)s
            RETURNING *
            """,
            {"id": source_id},
        )

        logger.info("Deleted source", extra={"source_id": source_id})
        return Source(**row) if row else None
