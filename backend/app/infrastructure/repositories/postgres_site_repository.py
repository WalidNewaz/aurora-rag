from typing import Optional, List
from app.domain.repositories.site_repository import SiteRepository
from app.domain.models.site import Site
from app.core.database import Database

class PostgresSiteRepository(SiteRepository):
    def __init__(self, db: Database):
        self.db = db

    async def get_by_url(self, url: str) -> Optional[Site]:
        row = await self.db.fetchone(
            "SELECT id, url, created_at FROM sites WHERE url = %(url)s",
            {"url": url}
        )
        return Site(**row) if row else None

    async def create(self, url: str) -> Site:
        row = await self.db.fetchone(
            """
            INSERT INTO sites (url)
            VALUES (%(url)s)
            RETURNING id, url, created_at
            """,
            {"url": url},
            True
        )
        return Site(**row)

    async def get_all(self) -> List[Site]:
        rows = await self.db.fetchall(
            "SELECT * FROM sites"
        )
        return rows

    async def get(self, site_id: int) -> Optional[Site]:
        row = await self.db.fetchone(
            "SELECT id, url, created_at FROM sites WHERE id = %(id)s",
            {"id": site_id}
        )
        return Site(**row) if row else None

    async def update(self, site_id: int, url: str) -> Site:
        row = await self.db.fetchone(
            "SELECT id, url, created_at FROM sites WHERE id = %(id)s",
            {"id": site_id}
        )
        return Site(**row) if row else None

    async def delete(self, site_id: int) -> None:
        row = await self.db.fetchone(
            "DELETE FROM sites WHERE id = %(id)s",
            {"id": site_id}
        )
        return row if row else None


