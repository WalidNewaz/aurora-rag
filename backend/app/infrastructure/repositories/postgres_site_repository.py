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

    async def create(self, url: str) -> SiteEntity:
        row = await self.db.fetchone(
            """
            INSERT INTO sites (url)
            VALUES (%(url)s)
            RETURNING *
            """,
            {"url": url},
            commit=True
        )
        return SiteEntity(**row)

    async def get_all(self) -> List[SiteEntity]:
        rows = await self.db.fetchall(
            "SELECT * FROM sites"
        )
        return [SiteEntity(**row) for row in rows]

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

        set_sql = ", ".join(set_clauses)

        query = f"""
                    UPDATE sites
                    SET {set_sql}
                    WHERE id = %(id)s
                    RETURNING *
                """

        row = await self.db.fetchone(query, params, commit=True)
        return SiteEntity(**row) if row else None

    async def delete(self, site_id: int) -> Optional[SiteEntity]:
        row = await self.db.fetchone(
            """
            DELETE FROM sites
            WHERE id = %(id)s
            RETURNING *
            """,
            {"id": site_id},
            commit=True
        )

        logger.info("Deleted site", extra={"site_id": site_id})
        return SiteEntity(**row) if row else None


