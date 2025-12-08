# --------------------------------
# DI container
# --------------------------------

from functools import lru_cache
from app.infrastructure.vector.dummy_retriever import DummyRetriever
from app.domain.services.retriever import Retriever

class Container:

    def __init__(self):
        self._retriever = DummyRetriever()

    @property
    def retriever(self) -> Retriever:
        return self._retriever

@lru_cache
def get_container():
    return Container()