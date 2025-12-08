from app.domain.services.crawler import Crawler
from app.infrastructure.crawling.http_fetcher import HttpFetcher
from app.infrastructure.crawling.html_parser import HtmlParser
from app.infrastructure.crawling.url_queue import UrlQueueRepository
from app.infrastructure.crawling.page_repository import PageRepository

class CrawlOrchestrator(Crawler):
    def __init__(self, db, site_repository):
        self.db = db
        self.site_repo = site_repository
        self.fetcher = HttpFetcher()
        self.parser = HtmlParser()

    async def crawl_site(self, site_id: str) -> None:
        site = await self.site_repo.get_site(site_id)
        queue = UrlQueueRepository(self.db)
        pages = PageRepository(self.db)

        # Seed the queue with the start_url
        await queue.add_url(site_id, site.start_url)

        while True:
            state = await queue.get_next_pending(site_id)
            if not state:
                break

            status, html = await self.fetcher.fetch(state.url)

            if status != 200 or html is None:
                await queue.mark_error(state.id, f"HTTP status: {status}")
                continue

            await pages.upsert_page(site_id, state.url, html)
            await queue.mark_success(state.id)

            # Extract links
            new_links = self.parser.extract_links(
                html,
                base_url=state.url,
                allowed_domains=site.allowed_domains
            )

            for link in new_links:
                await queue.add_url(site_id, link)


    async def submit_site(self, url: str):
        site = await self.site_repo.get_by_url(url)
        if not site:
            site = await self.site_repo.create(url)
        return site