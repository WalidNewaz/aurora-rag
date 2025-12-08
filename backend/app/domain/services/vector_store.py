from abc import ABC, abstractmethod
from typing import Iterable
from app.domain.models.chunk import Chunk

class VectorStore(ABC):

    @abstractmethod
    async def upsert(self, chunks: Iterable[Chunk]) -> None:
        ...

    @abstractmethod
    async def search(self, query_embedding: list[float], k: int = 5) -> list[Chunk]:
        ...

    @abstractmethod
    async def delete_by_site(self, site_id: str) -> None:
        ...