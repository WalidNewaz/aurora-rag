from dataclasses import dataclass
from datetime import datetime

@dataclass
class CrawlState:
    id: str
    site_id: str
    url: str
    status: str  # pending, success, error
    discovered_at: datetime
    fetched_at: datetime | None
    last_error: str | None