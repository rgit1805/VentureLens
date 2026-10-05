from google import genai
from google.genai import types

from app.ai.embeddings.base import EmbeddingProvider
from app.core.config import settings


class GeminiEmbeddingProvider(EmbeddingProvider):
    """Gemini-based implementation of the embedding provider."""

    def __init__(self, client=None) -> None:
        if client is not None:
            self.client = client
            return

        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(
            api_key=settings.gemini_api_key,
        )

    def embed_text(self, text: str) -> list[float]:
        if not text.strip():
            raise ValueError("Text cannot be empty.")

        result = self.client.models.embed_content(
            model=settings.embedding_model,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=settings.embedding_dimension,
            ),
        )

        if not result.embeddings:
            raise ValueError("Gemini returned no embedding.")

        embedding = result.embeddings[0].values

        if embedding is None:
            raise ValueError("Gemini returned an empty embedding vector.")

        if len(embedding) != settings.embedding_dimension:
            raise ValueError(
                "Unexpected embedding dimension: "
                f"expected {settings.embedding_dimension}, "
                f"got {len(embedding)}"
            )

        return list(embedding)