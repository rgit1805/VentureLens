from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document_chunk import DocumentChunk
from app.services.documents.chunking import DocumentChunkData


class DocumentChunkPersistenceError(ValueError):
    """Raised when chunk data cannot safely be persisted."""


class DocumentChunkPersistenceService:
    """Persist and replace the chunks belonging to a document."""

    def persist_document_chunks(
        self,
        db: Session,
        document_id: UUID,
        chunks: list[DocumentChunkData],
    ) -> int:
        """
        Replace a document's existing chunks atomically.

        Existing chunks are retained if validation fails or the database
        transaction fails. Returns the number of newly persisted chunks.
        """

        self._validate_chunks(chunks)

        records = [
            DocumentChunk(
                document_id=document_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                page_number=chunk.page_number,
                source_location=chunk.source_location,
            )
            for chunk in chunks
        ]

        try:
            (
                db.query(DocumentChunk)
                .filter(DocumentChunk.document_id == document_id)
                .delete(synchronize_session=False)
            )

            db.add_all(records)
            db.commit()

            return len(records)

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def _validate_chunks(chunks: list[DocumentChunkData]) -> None:
        if not chunks:
            raise DocumentChunkPersistenceError(
                "Cannot persist an empty chunk list."
            )

        indexes = [chunk.chunk_index for chunk in chunks]

        if any(index < 0 for index in indexes):
            raise DocumentChunkPersistenceError(
                "Chunk indexes cannot be negative."
            )

        if len(indexes) != len(set(indexes)):
            raise DocumentChunkPersistenceError(
                "Chunk indexes must be unique within a document."
            )

        if set(indexes) != set(range(len(chunks))):
            raise DocumentChunkPersistenceError(
                "Chunk indexes must be sequential, starting from zero."
            )

        if any(not chunk.content or not chunk.content.strip() for chunk in chunks):
            raise DocumentChunkPersistenceError(
                "Chunk content cannot be empty."
            )