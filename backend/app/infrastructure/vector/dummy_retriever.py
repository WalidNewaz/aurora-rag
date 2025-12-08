from app.domain.services.retriever import Retriever
from app.domain.models.chunk import Chunk

class DummyRetriever(Retriever):
    async def retrieve(self, query: str, k: int = 5):
        return [
            Chunk(
                id="test",
                document_id="doc1",
                site_id="site1",
                text="Dummy chunk for testing.",
                embedding=None,
                chunk_index=0,
                created_at=None,
                updated_at=None
            )
        ]