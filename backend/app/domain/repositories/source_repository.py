from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.source import Source


class SourceRepository(ABC):

    @abstractmethod
    async def create(
        self,
        *,
        type: str,
        name: str | None,
        config: dict,
    ) -> Source:
        ...

    @abstractmethod
    async def get(self, source_id: int) -> Optional[Source]:
        ...

    @abstractmethod
    async def delete(self, source_id: int) -> Optional[Source]:
        ...
