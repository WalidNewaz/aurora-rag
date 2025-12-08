from dataclasses import dataclass
from datetime import datetime

@dataclass
class Chunk:
    id: str
    document_id: str
    site_id: str
    text: str
    embedding: list[float] | None
    chunk_index: int
    created_at: datetime
    updated_at: datetime