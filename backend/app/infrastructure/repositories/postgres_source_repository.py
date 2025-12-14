from __future__ import annotations

from typing import Optional, Any
import psycopg
from psycopg.types.json import Json

from app.domain.repositories.source_repository import SourceRepository
from app.domain.models.source import Source
from app.core.database import Database
from app.core.logging import logger


# Constants
ALLOWED_UPDATE_FIELDS = {
    "name",
    "config",
}


class PostgresSourceRepository(SourceRepository):
    def __init__(self, db: Database):
        self.db = db

    async def create(
            self,
            *,
            type: str,
            name: str | None,
            config: dict,
            conn: psycopg.AsyncConnection
    ) -> Source:
        query = """
            INSERT INTO sources (type, name, config)
            VALUES (%(type)s, %(name)s, %(config)s)
            RETURNING *
            """
        params = {
                "type": type,
                "name": name,
                "config": Json(config),
            }
        row = await self._fetchone(query, params, conn=conn)
        return Source(**row)

    async def get_all(
            self,
            *,
            conn: psycopg.AsyncConnection
    ) -> list[Source]:
        query = "SELECT * FROM sources"
        rows = await self._fetchall(query, conn=conn)
        return [Source(**row) for row in rows]

    async def get(
            self,
            source_id: int,
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Source]:
        query = "SELECT * FROM sources WHERE id = %(source_id)s"
        params = {"source_id": source_id}
        row = await self._fetchone(query, params, conn=conn)
        return Source(**row) if row else None

    async def update(
            self,
            source_id: int,
            updates: dict[str, Any],
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Source]:
        update_data = {
            k: v for k, v in updates.items()
            if k in ALLOWED_UPDATE_FIELDS
        }

        if not update_data:
            return None

        set_clauses = []
        params = {"id": source_id}

        for field, value in update_data.items():
            set_clauses.append(f"{field} = %({field})s")
            if field == "config" and isinstance(value, dict):
                params[field] = Json(value)
            else:
                params[field] = value

        query = f"""
                    UPDATE sources
                    SET {", ".join(set_clauses)}
                    WHERE id = %(id)s
                    RETURNING *
                """

        row = await self._fetchone(query, params, conn=conn)
        return Source(**row) if row else None

    async def delete(
            self,
            source_id: int,
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Source]:
        query = """
            DELETE FROM sources
            WHERE id = %(id)s
            RETURNING *
            """
        params = {"id": source_id}
        row = await self._fetchone(query, params, conn=conn)

        logger.info("Deleted source", extra={"source_id": source_id})
        return Source(**row) if row else None

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


    async def _fetchall(
            self,
            query: str,
            *,
            conn: psycopg.AsyncConnection | None,
    ):
        if conn is None:
            return await self.db.fetchall()

        async with conn.cursor() as cur:
            await cur.execute(query)
            return await cur.fetchall()
