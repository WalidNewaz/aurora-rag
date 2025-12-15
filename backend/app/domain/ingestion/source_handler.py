from abc import ABC, abstractmethod

from app.domain.models.source import Source

class SourceHandler(ABC):
    """
    Source handler abstract base class.
    Source handlers handle updating the proper source
    type table, when the actual source config is updated.
    """

    @abstractmethod
    async def on_created(self, source: Source) -> None:
        ...

    @abstractmethod
    async def on_updated(self, source: Source) -> None:
        ...

    @abstractmethod
    async def on_deleted(self, source: Source) -> None:
        ...

