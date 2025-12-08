import uuid
import hashlib
from datetime import datetime

class PageRepository:
    def __init__(self, db):
        self.db = db

    @staticmethod
    def compute_checksum(html: str) -> str:
        return hashlib.sha256(html.encode()).hexdigest()

    async def upsert_page(self, site_id: str, url: str, raw_html: str) -> None:
        checksum = self.compute_checksum(raw_html)

        await self.db.execute(
            """
            INSERT INTO pages (id, site_id, url, raw_html, fetched_at, checksum)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (site_id, url)
            DO UPDATE SET raw_html=$4, fetched_at=$5, checksum=$6
            """,
            str(uuid.uuid4()), site_id, url, raw_html, datetime.utcnow(), checksum
        )