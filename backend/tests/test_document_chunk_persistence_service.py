from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import pytest

from app.db.models.document_chunk import DocumentChunk
from app.services.document_chunk_persistence_service import (
    DocumentChunkPersistenceError,
    DocumentChunkPersistenceService,
)


def make_chunks():
    return [
        SimpleNamespace(
            chunk_index=0,
            content="Company overview",
            page_number=1,
            source_location="page:1",
        ),
        SimpleNamespace(
            chunk_index=1,
            content="Financial performance",
            page_number=2,
            source_location="page:2",
        ),
    ]


def make_db():
    query = Mock()
    query.filter.return_value = query
    query.delete.return_value = 0

    db = Mock()
    db.query.return_value = query

    return db, query


def test_persists_document_chunks():
    db, query = make_db()
    service = DocumentChunkPersistenceService()
    document_id = uuid4()
    chunks = make_chunks()

    count = service.persist_document_chunks(
        db=db,
        document_id=document_id,
        chunks=chunks,
    )

    assert count == 2

    query.delete.assert_called_once_with(
        synchronize_session=False
    )

    db.add_all.assert_called_once()

    records = db.add_all.call_args.args[0]

    assert len(records) == 2

    assert records[0].document_id == document_id
    assert records[0].chunk_index == 0
    assert records[0].content == "Company overview"
    assert records[0].page_number == 1
    assert records[0].source_location == "page:1"
    assert records[0].embedding is None

    assert records[1].document_id == document_id
    assert records[1].chunk_index == 1
    assert records[1].content == "Financial performance"
    assert records[1].page_number == 2
    assert records[1].source_location == "page:2"
    assert records[1].embedding is None

    db.commit.assert_called_once()
    db.rollback.assert_not_called()
    db.query.assert_called_once_with(DocumentChunk)


def test_rejects_empty_chunk_list():
    db, _ = make_db()
    service = DocumentChunkPersistenceService()

    with pytest.raises(
        DocumentChunkPersistenceError,
        match="empty chunk list",
    ):
        service.persist_document_chunks(
            db=db,
            document_id=uuid4(),
            chunks=[],
        )

    db.query.assert_not_called()
    db.add_all.assert_not_called()
    db.commit.assert_not_called()


def test_rejects_duplicate_chunk_indexes():
    db, _ = make_db()
    service = DocumentChunkPersistenceService()
    chunks = make_chunks()
    chunks[1].chunk_index = 0

    with pytest.raises(
        DocumentChunkPersistenceError,
        match="unique",
    ):
        service.persist_document_chunks(
            db=db,
            document_id=uuid4(),
            chunks=chunks,
        )

    db.query.assert_not_called()


def test_rejects_negative_chunk_indexes():
    db, _ = make_db()
    service = DocumentChunkPersistenceService()
    chunks = make_chunks()
    chunks[0].chunk_index = -1

    with pytest.raises(
        DocumentChunkPersistenceError,
        match="negative",
    ):
        service.persist_document_chunks(
            db=db,
            document_id=uuid4(),
            chunks=chunks,
        )

    db.query.assert_not_called()


def test_rejects_non_sequential_chunk_indexes():
    db, _ = make_db()
    service = DocumentChunkPersistenceService()
    chunks = make_chunks()
    chunks[1].chunk_index = 3

    with pytest.raises(
        DocumentChunkPersistenceError,
        match="sequential",
    ):
        service.persist_document_chunks(
            db=db,
            document_id=uuid4(),
            chunks=chunks,
        )

    db.query.assert_not_called()


def test_rejects_blank_chunk_content():
    db, _ = make_db()
    service = DocumentChunkPersistenceService()
    chunks = make_chunks()
    chunks[0].content = "   "

    with pytest.raises(
        DocumentChunkPersistenceError,
        match="content",
    ):
        service.persist_document_chunks(
            db=db,
            document_id=uuid4(),
            chunks=chunks,
        )

    db.query.assert_not_called()


def test_rolls_back_when_database_insert_fails():
    db, _ = make_db()
    service = DocumentChunkPersistenceService()

    db.add_all.side_effect = RuntimeError("database insert failed")

    with pytest.raises(
        RuntimeError,
        match="database insert failed",
    ):
        service.persist_document_chunks(
            db=db,
            document_id=uuid4(),
            chunks=make_chunks(),
        )

    db.commit.assert_not_called()
    db.rollback.assert_called_once()


def test_rolls_back_when_database_commit_fails():
    db, _ = make_db()
    service = DocumentChunkPersistenceService()

    db.commit.side_effect = RuntimeError("database commit failed")

    with pytest.raises(
        RuntimeError,
        match="database commit failed",
    ):
        service.persist_document_chunks(
            db=db,
            document_id=uuid4(),
            chunks=make_chunks(),
        )

    db.add_all.assert_called_once()
    db.commit.assert_called_once()
    db.rollback.assert_called_once()