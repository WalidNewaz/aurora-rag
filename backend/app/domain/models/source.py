from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Source:
    id: int
    type: str
    name: str | None
    config: dict[str, Any]
    created_at: datetime
