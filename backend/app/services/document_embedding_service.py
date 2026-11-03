from uuid import UUID

from sqlalchemy.orm import Session

from app.ai.embeddings.service import EmbeddingService
from app.db.models.document_chunk import DocumentChunk


class DocumentEmbeddingService:
    """Generate and persist embeddings for a document's unembedded chunks."""

    def __init__(self, embedding_service: EmbeddingService) -> None:
        self.embedding_service = embedding_service

    def embed_document_chunks(self, db: Session, document_id: UUID) -> int:
        """Persist embeddings atomically; return the number of updated chunks.

        Existing embeddings are left untouched. All vectors are generated and
        validated before any ORM objects are modified, then committed together.
        """
        chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id,
                DocumentChunk.embedding.is_(None),
            )
            .order_by(DocumentChunk.chunk_index.asc())
            .all()
        )

        if not chunks:
            return 0

        try:
            vectors = self.embedding_service.embed_texts(
                [chunk.content for chunk in chunks]
            )

            if len(vectors) != len(chunks):
                raise ValueError(
                    "Embedding service returned a different number of vectors "
                    "than requested chunks."
                )

            for chunk, vector in zip(chunks, vectors, strict=True):
                chunk.embedding = vector

            db.commit()
            return len(chunks)
        except Exception:
            db.rollback()
            raise
