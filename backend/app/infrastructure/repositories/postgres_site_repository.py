from typing import Optional, List, Any

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

    async def get_by_url(self, url: str) -> Optional[SiteEntity]:
        row = await self.db.fetchone(
            "SELECT * FROM sites WHERE url = %(url)s",
            {"url": url}
        )
        return SiteEntity(**row) if row else None

    async def get_all(self) -> List[SiteEntity]:
        rows = await self.db.fetchall(
            "SELECT * FROM sites"
        )
        return [SiteEntity(**row) for row in rows]

    async def create(
            self,
            url: str,
            source_id: int,
            name: str = "",
            start_url: str = "",
            allowed_domains: List[str] | None = None,
            max_depth: int = 2,
    ) -> SiteEntity:
        row = await self.db.fetchone(
            """
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
            """,
            {
                "url": url,
                "source_id": source_id,
                "name": name,
                "start_url": start_url,
                "allowed_domains": allowed_domains or [],
                "max_depth": max_depth,
            },
        )
        return SiteEntity(**row)

    async def get(self, site_id: int) -> Optional[SiteEntity]:
        row = await self.db.fetchone(
            "SELECT * FROM sites WHERE id = %(id)s",
            {"id": site_id}
        )
        return SiteEntity(**row) if row else None

    async def update(
            self,
            site_id: int,
            updates: dict[str, Any],
    ) -> Optional[SiteEntity]:
        update_data = {
            k: v for k, v in updates.items()
            if k in ALLOWED_UPDATE_FIELDS
        }

        if not update_data:
            return None

        set_clauses = []
        params = {"id": site_id}

        for field, value in update_data.items():
            set_clauses.append(f"{field} = %({field})s")
            params[field] = value

        query = f"""
                    UPDATE sites
                    SET {", ".join(set_clauses)}
                    WHERE id = %(id)s
                    RETURNING *
                """

        row = await self.db.fetchone(query, params)
        return SiteEntity(**row) if row else None

    async def delete(self, site_id: int) -> Optional[SiteEntity]:
        row = await self.db.fetchone(
            """
            DELETE FROM sites
            WHERE id = %(id)s
            RETURNING *
            """,
            {"id": site_id},
        )

        logger.info("Deleted site", extra={"site_id": site_id})
        return SiteEntity(**row) if row else None


