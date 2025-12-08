from abc import ABC, abstractmethod
from app.domain.models.chunk import Chunk

class Retriever(ABC):

    @abstractmethod
    async def retrieve(self, query: str, k: int = 5) -> list[Chunk]:
        ...