# --------------------------------
# DI container
# --------------------------------

from functools import lru_cache

from app.infrastructure.vector.dummy_retriever import DummyRetriever
from app.domain.services.retriever import Retriever
from app.infrastructure.vector.dummy_embedding_provider import DummyEmbeddingProvider
from app.domain.services.embedding_provider import EmbeddingProvider

class Container:

    def __init__(self):
        self._retriever = DummyRetriever()
        self._embedding_provider = DummyEmbeddingProvider()

    @property
    def retriever(self) -> Retriever:
        return self._retriever

    @property
    def embedding_provider(self) -> EmbeddingProvider:
        return self._embedding_provider

@lru_cache
def get_container():
    return Container()