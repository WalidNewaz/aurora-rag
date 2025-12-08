from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.site import Site

class SiteRepository(ABC):

    @abstractmethod
    async def get_by_url(self, url: str) -> Optional[Site]:
        ...

    @abstractmethod
    async def create(self, url: str) -> Site:
        ...

    @abstractmethod
    async def get(self, site_id: int) -> Optional[Site]:
        ...
