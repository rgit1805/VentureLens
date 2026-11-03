
from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import MagicMock

import pytest

from app.db.models.document import Document

from app.services.document_processing_service import (
    DocumentProcessingService,
    DocumentNotFoundError,
    DocumentProcessingError,
    DocumentAlreadyProcessingError,
    DocumentAlreadyProcessedError,
)


def build_processing_service(
    existing_chunks=0,
    unembedded_chunks=0,
):
    document_id = uuid4()

    document = SimpleNamespace(
        id=document_id,
        filename="report.txt",
        storage_path="storage/report.txt",
        processing_status="pending",
        processing_error=None,
    )

    db = MagicMock()

    document_query = MagicMock()
    document_query.filter.return_value.first.return_value = document

    # Support SELECT FOR UPDATE queries.
    document_query.filter.return_value.with_for_update.return_value.first.return_value = (
        document
    )

    chunk_query = MagicMock()
    chunk_query.filter.return_value.count.side_effect = [
        existing_chunks,
        unembedded_chunks,
    ]

    def query_side_effect(model):
        if model is Document:
            return document_query

        return chunk_query

    db.query.side_effect = query_side_effect

    storage = MagicMock()
    storage.read_file.return_value = b"VentureLens document content"

    extraction_service = MagicMock()
    extraction_service.extract.return_value = [
        SimpleNamespace(
            text="VentureLens investment report",
            page_number=1,
            source_location="page:1",
        )
    ]

    chunking_service = MagicMock()
    chunking_service.chunk_sections.return_value = [
        SimpleNamespace(
            chunk_index=0,
            content="VentureLens investment report",
            page_number=1,
            source_location="page:1",
        )
    ]

    chunk_persistence_service = MagicMock()
    chunk_persistence_service.persist_document_chunks.return_value = 1

    embedding_service = MagicMock()
    embedding_service.embed_document_chunks.return_value = 1

    service = DocumentProcessingService(
        storage=storage,
        extraction_service=extraction_service,
        chunking_service=chunking_service,
        chunk_persistence_service=chunk_persistence_service,
        embedding_service=embedding_service,
    )

    return {
        "service": service,
        "db": db,
        "document": document,
        "document_id": document_id,
        "document_query": document_query,
        "storage": storage,
        "extraction": extraction_service,
        "chunking": chunking_service,
        "persistence": chunk_persistence_service,
        "embedding": embedding_service,
    }


def test_processes_document_successfully():
    context = build_processing_service()

    result = context["service"].process_document(
        context["db"],
        context["document_id"],
    )

    assert result.document_id == context["document_id"]
    assert result.chunks_persisted == 1
    assert result.embeddings_generated == 1
    assert result.reused_existing_chunks is False
    assert result.processing_status == "completed"

    assert context["document"].processing_status == "completed"
    assert context["document"].processing_error is None

    context["storage"].read_file.assert_called_once()
    context["extraction"].extract.assert_called_once()
    context["chunking"].chunk_sections.assert_called_once()
    context["persistence"].persist_document_chunks.assert_called_once()
    context["embedding"].embed_document_chunks.assert_called_once()


def test_raises_error_when_document_does_not_exist():
    context = build_processing_service()

    context[
        "document_query"
    ].filter.return_value.with_for_update.return_value.first.return_value = None

    with pytest.raises(DocumentNotFoundError):
        context["service"].process_document(
            context["db"],
            context["document_id"],
        )

    context["storage"].read_file.assert_not_called()
    context["db"].commit.assert_not_called()


def test_marks_document_failed_when_storage_read_fails():
    context = build_processing_service()

    context["storage"].read_file.side_effect = FileNotFoundError(
        "Stored file is missing"
    )

    with pytest.raises(DocumentProcessingError):
        context["service"].process_document(
            context["db"],
            context["document_id"],
        )

    assert context["document"].processing_status == "failed"
    assert "FileNotFoundError" in context["document"].processing_error

    context["db"].rollback.assert_called_once()


def test_rejects_document_with_no_generated_chunks():
    context = build_processing_service()

    context["chunking"].chunk_sections.return_value = []

    with pytest.raises(
        DocumentProcessingError,
        match="no usable text chunks",
    ):
        context["service"].process_document(
            context["db"],
            context["document_id"],
        )

    assert context["document"].processing_status == "failed"
    context["persistence"].persist_document_chunks.assert_not_called()
    context["embedding"].embed_document_chunks.assert_not_called()


def test_marks_document_failed_when_chunk_persistence_fails():
    context = build_processing_service()

    context["persistence"].persist_document_chunks.side_effect = RuntimeError(
        "Database insert failed"
    )

    with pytest.raises(DocumentProcessingError):
        context["service"].process_document(
            context["db"],
            context["document_id"],
        )

    assert context["document"].processing_status == "failed"
    context["embedding"].embed_document_chunks.assert_not_called()


def test_preserves_chunks_when_embedding_generation_fails():
    context = build_processing_service()

    context["embedding"].embed_document_chunks.side_effect = RuntimeError(
        "Embedding provider unavailable"
    )

    with pytest.raises(DocumentProcessingError):
        context["service"].process_document(
            context["db"],
            context["document_id"],
        )

    assert context["document"].processing_status == "failed"

    context["persistence"].persist_document_chunks.assert_called_once()
    context["db"].rollback.assert_called_once()


def test_retry_reuses_existing_chunks():
    context = build_processing_service(
        existing_chunks=3,
        unembedded_chunks=0,
    )

    context["embedding"].embed_document_chunks.return_value = 3

    result = context["service"].process_document(
        context["db"],
        context["document_id"],
    )

    assert result.reused_existing_chunks is True
    assert result.chunks_persisted == 0
    assert result.embeddings_generated == 3
    assert result.processing_status == "completed"

    context["storage"].read_file.assert_not_called()
    context["extraction"].extract.assert_not_called()
    context["chunking"].chunk_sections.assert_not_called()
    context["persistence"].persist_document_chunks.assert_not_called()


def test_already_embedded_document_does_not_regenerate_embeddings():
    context = build_processing_service(
        existing_chunks=3,
        unembedded_chunks=0,
    )

    context["embedding"].embed_document_chunks.return_value = 0

    result = context["service"].process_document(
        context["db"],
        context["document_id"],
    )

    assert result.embeddings_generated == 0
    assert result.reused_existing_chunks is True
    assert result.processing_status == "completed"

    context["embedding"].embed_document_chunks.assert_called_once()


def test_rejects_document_already_being_processed():
    context = build_processing_service()

    context["document"].processing_status = "processing"

    with pytest.raises(DocumentAlreadyProcessingError):
        context["service"].process_document(
            context["db"],
            context["document_id"],
        )

    context["storage"].read_file.assert_not_called()
    context["db"].commit.assert_not_called()


def test_rejects_already_completed_document():
    context = build_processing_service()

    context["document"].processing_status = "completed"

    with pytest.raises(DocumentAlreadyProcessedError):
        context["service"].process_document(
            context["db"],
            context["document_id"],
        )

    context["storage"].read_file.assert_not_called()
    context["db"].commit.assert_not_called()

