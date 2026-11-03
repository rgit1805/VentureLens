from math import isfinite
from typing import Sequence

from app.ai.embeddings.base import EmbeddingProvider
from app.core.config import settings


class EmbeddingService:
    """Application-level orchestration for generating text embeddings."""

    def __init__(
        self,
        provider: EmbeddingProvider,
        expected_dimension: int | None = None,
    ) -> None:
        dimension = (
            settings.embedding_dimension
            if expected_dimension is None
            else expected_dimension
        )
        if dimension <= 0:
            raise ValueError("Embedding dimension must be greater than zero.")

        self.provider = provider
        self.expected_dimension = dimension

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        """Generate one validated embedding for each input text.

        Provider exceptions are intentionally allowed to propagate so callers
        can apply retry, logging, or job-failure policies at the appropriate
        application boundary.
        """
        if isinstance(texts, (str, bytes)) or not isinstance(texts, Sequence):
            raise TypeError("texts must be a sequence of strings.")

        if not texts:
            raise ValueError("At least one text is required.")

        embeddings: list[list[float]] = []
        for index, text in enumerate(texts):
            if not isinstance(text, str):
                raise TypeError(f"Text at index {index} must be a string.")
            if not text.strip():
                raise ValueError(f"Text at index {index} cannot be empty.")

            raw_embedding = self.provider.embed_text(text)
            embeddings.append(self._validate_embedding(raw_embedding, index))

        return embeddings

    def _validate_embedding(
        self,
        embedding: Sequence[float],
        text_index: int,
    ) -> list[float]:
        if not isinstance(embedding, (list, tuple)):
            raise ValueError(
                f"Provider returned an invalid embedding for text at index {text_index}."
            )

        if len(embedding) != self.expected_dimension:
            raise ValueError(
                f"Embedding at index {text_index} has dimension {len(embedding)}; "
                f"expected {self.expected_dimension}."
            )

        validated: list[float] = []
        for value_index, value in enumerate(embedding):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(
                    f"Embedding value at index {text_index}, position {value_index} "
                    "must be numeric."
                )
            numeric_value = float(value)
            if not isfinite(numeric_value):
                raise ValueError(
                    f"Embedding value at index {text_index}, position {value_index} "
                    "must be finite."
                )
            validated.append(numeric_value)

        return validated
