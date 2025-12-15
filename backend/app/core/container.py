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

# Repositories
from app.domain.repositories.site_repository import SiteRepository
from app.infrastructure.repositories.postgres_site_repository import PostgresSiteRepository
from app.domain.repositories.source_repository import SourceRepository
from app.infrastructure.repositories.postgres_source_repository import PostgresSourceRepository

# Source Handlers
from app.application.ingestion.ingestion_coordinator import IngestionCoordinator
from app.domain.ingestion.source_handler import SourceHandler
from app.infrastructure.ingestion.handlers.web_source_handler import WebSourceHandler

# Artifact Handlers
from app.application.artifacts.artifact_service import ArtifactService
from app.infrastructure.repositories.postgres_artifact_repository import PostgresArtifactRepository


class Container:

    def __init__(self, settings):
        self._settings = settings
        self._db = Database(self._settings.database_url)
        # repositories
        self._site_repository = PostgresSiteRepository(self._db)
        self._source_repository = PostgresSourceRepository(self._db)
        # source handlers
        self._web_source_handler = WebSourceHandler(
            site_repo = self._site_repository
        )
        self._ingestion_coordinator = IngestionCoordinator(
            handlers={
                "web": self._web_source_handler,
            }
        )
        # artifact handler
        self._artifact_repository = PostgresArtifactRepository()
        self._artifact_service = ArtifactService(
            artifact_repo=self._artifact_repository,
            upload_root=settings.upload_dir,
        )
        # crawlers
        self._crawl_orchestrator = CrawlOrchestrator(db=self._db, site_repository=self._site_repository)
        # embedder
        self._embedding_provider = DummyEmbeddingProvider()
        # retriever
        self._retriever = DummyRetriever()


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

    @property
    def ingestion_coordinator(self) -> IngestionCoordinator:
        return self._ingestion_coordinator

    @property
    def artifact_service(self) -> ArtifactService:
        return self._artifact_service

@lru_cache
def get_container():
    return Container(settings)