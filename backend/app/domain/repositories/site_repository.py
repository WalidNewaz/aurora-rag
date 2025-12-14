from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.models.site import Site

class SiteRepository(ABC):

    @abstractmethod
    async def get_by_url(
            self,
            url: str,
    ) -> Optional[Site]:
        ...

    @abstractmethod
    async def get_all(self) -> List[Site]:
        ...

    @abstractmethod
    async def create(
            self,
            url: str,
            source_id: int,
            name: str = "",
            start_url: str = "",
            allowed_domains: List[str] | None = None,
            max_depth: int = 2,
    ) -> Site:
        ...

    @abstractmethod
    async def get(self, site_id: int) -> Optional[Site]:
        ...
