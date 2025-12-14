from __future__ import annotations

from typing import Optional, List, Any

import psycopg

from app.domain.repositories.site_repository import SiteRepository
from app.domain.models.site import Site as SiteEntity
from app.core.database import Database
from app.core.logging import logger

# Constants
ALLOWED_UPDATE_FIELDS = {
    "url",
    "name",
    "start_url",
    "allowed_domains",
    "max_depth",
    "last_crawled_at",
}

class PostgresSiteRepository(SiteRepository):
    def __init__(self, db: Database):
        self.db = db

    async def create(
            self,
            *,
            url: str,
            source_id: int,
            name: str = "",
            start_url: str = "",
            allowed_domains: List[str] | None = None,
            max_depth: int = 2,
            conn: psycopg.AsyncConnection | None = None,
    ) -> SiteEntity:
        query = """
            INSERT INTO sites (
                url,
                source_id,
                name,
                start_url,
                allowed_domains,
                max_depth
            )
            VALUES (
                %(url)s,
                %(source_id)s,
                %(name)s,
                %(start_url)s,
                %(allowed_domains)s,
                %(max_depth)s
            )
            RETURNING *
            """
        params = {
                "url": url,
                "source_id": source_id,
                "name": name,
                "start_url": start_url,
                "allowed_domains": allowed_domains or [],
                "max_depth": max_depth,
            }
        row = await self._fetchone(query, params, conn=conn)
        logger.info("Created site", extra={"site_id": row["id"]})
        return SiteEntity(**row)

    async def get_all(
            self,
            *,
            conn: psycopg.AsyncConnection | None = None
    ) -> List[SiteEntity]:
        query = "SELECT * FROM sites"
        rows = await self._fetchall(query, conn=conn)
        return [SiteEntity(**row) for row in rows]

    async def get(
            self,
            site_id: int,
            *,
            conn: psycopg.AsyncConnection | None = None
    ) -> Optional[SiteEntity]:
        query = "SELECT * FROM sites WHERE id = %(site_id)s"
        params = {"site_id": site_id}
        row = await self._fetchone(query, params, conn=conn)
        return SiteEntity(**row) if row else None

    async def get_by_url(
            self,
            url: str,
            *,
            conn: psycopg.AsyncConnection | None = None
    ) -> Optional[SiteEntity]:
        query = "SELECT * FROM sites WHERE url = %(url)s"
        params = {"url": url}
        row = await self._fetchone(query, params, conn=conn)
        return SiteEntity(**row) if row else None

    async def get_by_source_id(
            self,
            source_id: int,
            *,
            conn: psycopg.AsyncConnection | None = None
    ) -> Optional[SiteEntity]:
        query = "SELECT * FROM sites WHERE source_id = %(source_id)s"
        params = {"source_id": source_id}
        row = await self._fetchone(query, params, conn=conn)
        return SiteEntity(**row) if row else None

    async def update(
            self,
            site_id: int,
            updates: dict[str, Any],
            *,
            conn: psycopg.AsyncConnection | None = None,
    ) -> Optional[SiteEntity]:
        update_data = {
            k: v for k, v in updates.items()
            if k in ALLOWED_UPDATE_FIELDS
        }
        if not update_data:
            return None

        set_sql = ", ".join([f"{k} = %({k})s" for k in update_data.keys()])
        params = {"id": site_id, **update_data}

        query = f"""
                    UPDATE sites
                    SET {set_sql}
                    WHERE id = %(id)s
                    RETURNING *
                """

        row = await self._fetchone(query, params, conn=conn)
        return SiteEntity(**row) if row else None

    async def delete(
            self,
            site_id: int,
            *,
            conn: psycopg.AsyncConnection | None = None,
    ) -> Optional[SiteEntity]:
        query = """
            DELETE FROM sites
            WHERE id = %(id)s
            RETURNING *
            """
        params = {"id": site_id}
        row = await self._fetchone(query, params, conn=conn)
        logger.info("Deleted site", extra={"site_id": site_id})
        return SiteEntity(**row) if row else None

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


