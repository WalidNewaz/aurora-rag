from dataclasses import dataclass
from datetime import datetime

@dataclass
class Document:
    id: str
    site_id: str
    url: str
    title: str
    raw_html: str
    text: str
    created_at: datetime
    updated_at: datetime