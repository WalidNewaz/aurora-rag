from abc import ABC, abstractmethod

class Crawler(ABC):

    @abstractmethod
    async def crawl_site(self, site_id: str) -> None:
        """Crawl all pages for a given site."""
        ...

    @abstractmethod
    async def submit_site(self, url: str) -> None:
        """Submit a site to crawl."""
        ...