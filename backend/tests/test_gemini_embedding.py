from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.ai.embeddings.gemini import GeminiEmbeddingProvider


def test_gemini_provider_returns_embedding():
    fake_vector = [0.1] * 768

    client = Mock()
    client.models.embed_content.return_value = SimpleNamespace(
        embeddings=[
            SimpleNamespace(
                values=fake_vector,
            )
        ]
    )

    provider = GeminiEmbeddingProvider()
    provider.client = client

    result = provider.embed_text(
        "VentureLens evaluates startup financial health."
    )

    assert result == fake_vector
    assert len(result) == 768

    client.models.embed_content.assert_called_once()


def test_gemini_provider_rejects_empty_text():
    provider = GeminiEmbeddingProvider.__new__(
        GeminiEmbeddingProvider
    )

    with pytest.raises(ValueError, match="Text cannot be empty"):
        provider.embed_text("   ")


def test_gemini_provider_rejects_wrong_dimension():
    fake_vector = [0.1] * 100

    client = Mock()
    client.models.embed_content.return_value = SimpleNamespace(
        embeddings=[
            SimpleNamespace(
                values=fake_vector,
            )
        ]
    )

    provider = GeminiEmbeddingProvider()
    provider.client = client

    with pytest.raises(ValueError, match="Unexpected embedding dimension"):
        provider.embed_text("Test startup information.")