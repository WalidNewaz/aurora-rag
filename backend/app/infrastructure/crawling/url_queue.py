import uuid
from datetime import datetime
from app.domain.models.crawl_state import CrawlState

class UrlQueueRepository:
    def __init__(self, db):
        self.db = db

    async def add_url(self, site_id: str, url: str) -> None:
        await self.db.execute(
            """
            INSERT INTO crawl_state (id, site_id, url, status, discovered_at)
            VALUES ($1, $2, $3, 'pending', $4)
            ON CONFLICT (site_id, url) DO NOTHING
            """,
            str(uuid.uuid4()), site_id, url, datetime.utcnow()
        )

    async def get_next_pending(self, site_id: str) -> CrawlState | None:
        row = await self.db.fetchrow(
            """
            SELECT * FROM crawl_state
            WHERE site_id=$1 AND status='pending'
            ORDER BY discovered_at ASC
            LIMIT 1
            """, site_id
        )

        if not row:
            return None

        return CrawlState(**row)

    async def mark_success(self, state_id: str) -> None:
        await self.db.execute(
            """
            UPDATE crawl_state SET status='success', fetched_at=$2 WHERE id=$1
            """,
            state_id, datetime.utcnow()
        )

    async def mark_error(self, state_id: str, error: str) -> None:
        await self.db.execute(
            """
            UPDATE crawl_state SET status='error', last_error=$2 WHERE id=$1
            """,
            state_id, error
        )