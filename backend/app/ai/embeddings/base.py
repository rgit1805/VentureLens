from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Contract for embedding providers."""

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text input."""
        raise NotImplementedError