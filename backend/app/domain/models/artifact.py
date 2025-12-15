from dataclasses import dataclass
from datetime import datetime

@dataclass
class Artifact:
    id: int
    source_id: int
    type: str           # upload | crawl | sync
    mime_type: str
    path: str
    size_bytes: int
    created_at: datetime
