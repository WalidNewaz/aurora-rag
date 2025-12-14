import psycopg
from abc import ABC, abstractmethod
from typing import Optional, List, Any

from app.domain.models.site import Site

class SiteRepository(ABC):

    @abstractmethod
    async def create(
            self,
            *,
            url: str,
            source_id: int,
            name: str = "",
            start_url: str = "",
            allowed_domains: List[str] | None = None,
            max_depth: int = 2,
            conn: psycopg.AsyncConnection
    ) -> Site:
        ...

    @abstractmethod
    async def get_all(
            self,
            *,
            conn: psycopg.AsyncConnection
    ) -> List[Site]:
        ...

    @abstractmethod
    async def get(
            self,
            site_id: int,
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Site]:
        ...

    @abstractmethod
    async def get_by_url(
            self,
            url: str,
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Site]:
        ...

    @abstractmethod
    async def get_by_source_id(
            self,
            source_id: int,
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Site]:
        ...

    @abstractmethod
    async def update(
            self,
            site_id: int,
            updates: dict[str, Any],
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Site]:
        ...

    @abstractmethod
    async def delete(
            self,
            site_id: int,
            *,
            conn: psycopg.AsyncConnection
    ) -> Optional[Site]:
        ...
