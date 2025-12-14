import psycopg
from abc import ABC, abstractmethod
from typing import Optional, Any
from app.domain.models.source import Source


class SourceRepository(ABC):

    @abstractmethod
    async def create(
            self,
            *,
            type: str,
            name: str | None,
            config: dict,
            conn: psycopg.AsyncConnection
    ) -> Source:
        ...

    @abstractmethod
    async def get_all(
            self,
            *,
            conn: psycopg.AsyncConnection
    ) -> list[Source]:
        ...

    @abstractmethod
    async def get(
            self,
            source_id: int,
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Source]:
        ...

    @abstractmethod
    async def update(
            self,
            source_id: int,
            updates: dict[str, Any],
            *,
            conn: psycopg.AsyncConnection
    ) -> Source:
        ...

    @abstractmethod
    async def delete(
            self,
            source_id: int,
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Source]:
        ...
