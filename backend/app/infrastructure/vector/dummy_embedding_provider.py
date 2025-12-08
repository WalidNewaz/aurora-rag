from app.domain.services.embedding_provider import EmbeddingProvider

class DummyEmbeddingProvider(EmbeddingProvider):
    async def embed(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [[0.1, 0.2, 0.3]]