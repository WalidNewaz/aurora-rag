from pydantic import BaseModel
from datetime import datetime

class Site(BaseModel):
    """The site registered"""
    id: int
    url: str
    name: str
    start_url: str
    allowed_domains: list[str]
    max_depth: int
    created_at: datetime
    last_crawled_at: datetime | None = None
    source_id: int = None

class SiteCreate(BaseModel):
    """A site being registered"""
    url: str
    name: str | None = None
    start_url: str | None = None
    allowed_domains: list[str] = []
    max_depth: int = 2

class SiteUpdate(BaseModel):
    """Mutable operational fields for a site"""
    start_url: str | None = None
    allowed_domains: list[str] | None = None
    max_depth: int | None = None
    last_crawled_at: datetime | None = None

