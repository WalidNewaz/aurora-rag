# --------------------------------
# DI container
# --------------------------------

from functools import lru_cache

from app.core.settings import settings
from app.infrastructure.vector.dummy_retriever import DummyRetriever
from app.domain.services.retriever import Retriever
from app.infrastructure.vector.dummy_embedding_provider import DummyEmbeddingProvider
from app.domain.services.embedding_provider import EmbeddingProvider
from app.application.use_cases.crawl_orchestrator import CrawlOrchestrator
from app.domain.services.crawler import Crawler
from app.core.database import Database

from app.domain.repositories.site_repository import SiteRepository
from app.infrastructure.repositories.postgres_site_repository import PostgresSiteRepository
from app.domain.repositories.source_repository import SourceRepository
from app.infrastructure.repositories.postgres_source_repository import PostgresSourceRepository


class Container:

    def __init__(self, settings):
        self._settings = settings
        self._db = Database(self._settings.database_url)
        self._retriever = DummyRetriever()
        self._embedding_provider = DummyEmbeddingProvider()
        self._site_repository = PostgresSiteRepository(self._db)
        self._source_repository = PostgresSourceRepository(self._db)
        self._crawl_orchestrator = CrawlOrchestrator(db=self._db, site_repository=self._site_repository)

    @property
    def db(self):
        return self._db

    @property
    def retriever(self) -> Retriever:
        return self._retriever

    @property
    def embedding_provider(self) -> EmbeddingProvider:
        return self._embedding_provider

    @property
    def crawl_orchestrator(self) -> Crawler:
        return self._crawl_orchestrator

    @property
    def site_repository(self) -> SiteRepository:
        return self._site_repository

    @property
    def source_repository(self) -> SourceRepository:
        return self._source_repository

@lru_cache
def get_container():
    return Container(settings)