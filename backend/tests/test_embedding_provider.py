import pytest

from app.ai.embeddings.base import EmbeddingProvider


class FakeEmbeddingProvider(EmbeddingProvider):
    def embed_text(self, text: str) -> list[float]:
        return [0.1, 0.2, 0.3]


def test_embedding_provider_contract():
    provider = FakeEmbeddingProvider()

    result = provider.embed_text("hello")

    assert result == [0.1, 0.2, 0.3]


def test_embedding_provider_requires_embed_text():
    with pytest.raises(TypeError):
        EmbeddingProvider()