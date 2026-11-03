from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.db.models.document_chunk import DocumentChunk
from app.services.document_embedding_service import DocumentEmbeddingService


def make_chunks():
    return [
        SimpleNamespace(chunk_index=0, content="Company overview", embedding=None),
        SimpleNamespace(chunk_index=1, content="Financial performance", embedding=None),
    ]


def make_db(chunks):
    query = Mock()
    query.filter.return_value = query
    query.order_by.return_value = query
    query.all.return_value = chunks

    db = Mock()
    db.query.return_value = query
    return db, query


def test_persists_embeddings_for_document_chunks_atomically():
    chunks = make_chunks()
    db, query = make_db(chunks)
    embedding_service = Mock()
    embedding_service.embed_texts.return_value = [[0.1, 0.2], [0.3, 0.4]]
    service = DocumentEmbeddingService(embedding_service)
    document_id = uuid4()

    count = service.embed_document_chunks(db, document_id)

    assert count == 2
    assert chunks[0].embedding == [0.1, 0.2]
    assert chunks[1].embedding == [0.3, 0.4]
    embedding_service.embed_texts.assert_called_once_with(
        ["Company overview", "Financial performance"]
    )
    db.commit.assert_called_once()
    db.rollback.assert_not_called()
    db.query.assert_called_once_with(DocumentChunk)
    query.all.assert_called_once()


def test_returns_zero_when_no_unembedded_chunks_exist():
    db, _ = make_db([])
    embedding_service = Mock()
    service = DocumentEmbeddingService(embedding_service)

    count = service.embed_document_chunks(db, uuid4())

    assert count == 0
    embedding_service.embed_texts.assert_not_called()
    db.commit.assert_not_called()
    db.rollback.assert_not_called()


def test_rolls_back_when_embedding_generation_fails():
    chunks = make_chunks()
    db, _ = make_db(chunks)
    embedding_service = Mock()
    embedding_service.embed_texts.side_effect = RuntimeError("provider unavailable")
    service = DocumentEmbeddingService(embedding_service)

    with pytest.raises(RuntimeError, match="provider unavailable"):
        service.embed_document_chunks(db, uuid4())

    assert all(chunk.embedding is None for chunk in chunks)
    db.commit.assert_not_called()
    db.rollback.assert_called_once()


def test_rolls_back_when_database_commit_fails():
    chunks = make_chunks()
    db, _ = make_db(chunks)
    embedding_service = Mock()
    embedding_service.embed_texts.return_value = [[0.1, 0.2], [0.3, 0.4]]
    db.commit.side_effect = RuntimeError("database unavailable")
    service = DocumentEmbeddingService(embedding_service)

    with pytest.raises(RuntimeError, match="database unavailable"):
        service.embed_document_chunks(db, uuid4())

    db.rollback.assert_called_once()
