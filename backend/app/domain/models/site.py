from dataclasses import dataclass
from datetime import datetime

@dataclass
class Site:
    id: str
    name: str
    start_url: str
    allowed_domains: list[str]
    created_at: datetime