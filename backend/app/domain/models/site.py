from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Site:
    id: str
    url: str
    name: str
    start_url: str
    allowed_domains: list[str]
    max_depth: int
    created_at: datetime
    last_crawled_at: datetime

@dataclass
class SiteUpdate:
    url: Optional[str] = None
    name: Optional[str] = None
    start_url: Optional[str] = None
    allowed_domains: Optional[list[str]] = None
    max_depth: Optional[int] = None
    last_crawled_at: Optional[datetime] = None