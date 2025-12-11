from dataclasses import dataclass
from datetime import datetime

@dataclass
class Site:
    id: str
    url: str
    name: str
    start_url: str
    allowed_domains: list[str]
    max_depth: int
    created_at: datetime