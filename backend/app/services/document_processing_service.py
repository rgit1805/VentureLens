
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.document import Document
from app.db.models.document_chunk import DocumentChunk
from app.services.documents.storage import DocumentStorage
from app.services.documents.extractors.service import (
    DocumentExtractionService,
)
from app.services.documents.chunking import DocumentChunkingService
from app.services.document_chunk_persistence_service import (
    DocumentChunkPersistenceService,
)
from app.services.document_embedding_service import (
    DocumentEmbeddingService,
)


class DocumentNotFoundError(Exception):
    """Raised when the requested document does not exist."""


class DocumentAlreadyProcessingError(Exception):
    """Raised when another worker is already processing the document."""


class DocumentAlreadyProcessedError(Exception):
    """Raised when the document has already been processed."""


class DocumentProcessingError(Exception):
    """Raised when document processing fails."""


@dataclass(frozen=True)
class DocumentProcessingResult:
    document_id: UUID
    chunks_persisted: int
    embeddings_generated: int
    reused_existing_chunks: bool
    processing_status: str


class DocumentProcessingService:
    """Coordinate extraction, chunking, persistence, and embedding."""

    def __init__(
        self,
        storage: DocumentStorage,
        extraction_service: DocumentExtractionService,
        chunking_service: DocumentChunkingService,
        chunk_persistence_service: DocumentChunkPersistenceService,
        embedding_service: DocumentEmbeddingService,
    ) -> None:
        self.storage = storage
        self.extraction_service = extraction_service
        self.chunking_service = chunking_service
        self.chunk_persistence_service = chunk_persistence_service
        self.embedding_service = embedding_service

    def process_document(
        self,
        db: Session,
        document_id: UUID,
    ) -> DocumentProcessingResult:

        # Atomically acquire the document row lock.
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .with_for_update()
            .first()
        )

        if document is None:
            raise DocumentNotFoundError(
                f"Document {document_id} was not found."
            )

        # Reject duplicate processing requests.
        if document.processing_status == "processing":
            raise DocumentAlreadyProcessingError(
                f"Document {document_id} is already being processed."
            )

        # Avoid unnecessarily processing completed documents.
        if document.processing_status == "completed":
            raise DocumentAlreadyProcessedError(
                f"Document {document_id} has already been processed."
            )

        # Only pending and failed documents can be claimed.
        if document.processing_status not in {"pending", "failed"}:
            raise DocumentProcessingError(
                f"Document {document_id} has an invalid processing status: "
                f"{document.processing_status}."
            )

        try:
            # Claim the document and release the row lock on commit.
            document.processing_status = "processing"
            document.processing_error = None
            db.commit()

            # Check whether chunks already exist.
            existing_chunks = (
                db.query(DocumentChunk.id)
                .filter(
                    DocumentChunk.document_id == document_id
                )
                .count()
            )

            reused_existing_chunks = existing_chunks > 0
            chunks_persisted = 0

            # Extract and persist chunks only when they do not exist.
            if not reused_existing_chunks:
                content = self.storage.read_file(
                    document.storage_path
                )

                sections = self.extraction_service.extract(
                    filename=document.filename,
                    content=content,
                )

                chunks = self.chunking_service.chunk_sections(
                    sections
                )

                if not chunks:
                    raise DocumentProcessingError(
                        "Document extraction produced no usable text chunks."
                    )

                chunks_persisted = (
                    self.chunk_persistence_service.persist_document_chunks(
                        db=db,
                        document_id=document_id,
                        chunks=chunks,
                    )
                )

            # Generate embeddings for chunks that do not have one.
            embeddings_generated = (
                self.embedding_service.embed_document_chunks(
                    db=db,
                    document_id=document_id,
                )
            )

            # Verify that no chunks remain without embeddings.
            unembedded_chunks = (
                db.query(DocumentChunk.id)
                .filter(
                    DocumentChunk.document_id == document_id,
                    DocumentChunk.embedding.is_(None),
                )
                .count()
            )

            if unembedded_chunks > 0:
                raise DocumentProcessingError(
                    f"{unembedded_chunks} document chunks remain unembedded."
                )

            # Mark processing as completed.
            document = (
                db.query(Document)
                .filter(Document.id == document_id)
                .first()
            )

            document.processing_status = "completed"
            document.processing_error = None
            db.commit()

            return DocumentProcessingResult(
                document_id=document_id,
                chunks_persisted=chunks_persisted,
                embeddings_generated=embeddings_generated,
                reused_existing_chunks=reused_existing_chunks,
                processing_status="completed",
            )

        except Exception as exc:
            db.rollback()

            # Record failure without retaining a failed transaction.
            failed_document = (
                db.query(Document)
                .filter(Document.id == document_id)
                .first()
            )

            if failed_document is not None:
                failed_document.processing_status = "failed"
                failed_document.processing_error = (
                    f"{type(exc).__name__}: {exc}"
                )[:4000]

                db.commit()

            if isinstance(exc, DocumentProcessingError):
                raise

            raise DocumentProcessingError(
                f"Processing failed for document {document_id}."
            ) from exc

