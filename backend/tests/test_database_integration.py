from sqlalchemy import text


def test_postgresql_integration_database(db_session):
    database_name = db_session.execute(
        text("SELECT current_database()")
    ).scalar_one()

    assert database_name == "venturelens_test"

    tables = db_session.execute(
        text("""
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public'
        """)
    ).scalars().all()

    assert "users" in tables
    assert "startups" in tables
    assert "documents" in tables
    assert "document_chunks" in tables
from types import SimpleNamespace
from uuid import uuid4

from app.db.models.user import User
from app.db.models.startup import Startup
from app.db.models.document import Document
from app.db.models.document_chunk import DocumentChunk
from app.services.document_chunk_persistence_service import (
    DocumentChunkPersistenceService,
)


def test_persists_document_chunks_in_postgresql(db_session):
    # Arrange: create the required ownership hierarchy.
    user = User(
        email=f"integration-{uuid4()}@example.com",
        password_hash="test-hash",
        full_name="Integration Test User",
    )
    db_session.add(user)
    db_session.flush()

    startup = Startup(
        owner_id=user.id,
        name="Integration Test Startup",
        industry="Technology",
        stage="Seed",
    )
    db_session.add(startup)
    db_session.flush()

    document = Document(
        startup_id=startup.id,
        filename="financial-report.txt",
        file_type="txt",
        storage_path="integration/financial-report.txt",
    )
    db_session.add(document)
    db_session.flush()

    chunks = [
        SimpleNamespace(
            chunk_index=0,
            content="Company overview and business model.",
            page_number=1,
            source_location="lines:1-5",
        ),
        SimpleNamespace(
            chunk_index=1,
            content="Revenue and financial performance.",
            page_number=2,
            source_location="lines:6-10",
        ),
    ]

    # Act: use the actual persistence service.
    service = DocumentChunkPersistenceService()

    count = service.persist_document_chunks(
        db=db_session,
        document_id=document.id,
        chunks=chunks,
    )

    # Assert: read the records back from PostgreSQL.
    stored_chunks = (
        db_session.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document.id)
        .order_by(DocumentChunk.chunk_index)
        .all()
    )

    assert count == 2
    assert len(stored_chunks) == 2

    assert stored_chunks[0].chunk_index == 0
    assert stored_chunks[0].content == (
        "Company overview and business model."
    )
    assert stored_chunks[0].page_number == 1
    assert stored_chunks[0].source_location == "lines:1-5"
    assert stored_chunks[0].embedding is None

    assert stored_chunks[1].chunk_index == 1
    assert stored_chunks[1].content == (
        "Revenue and financial performance."
    )
    assert stored_chunks[1].page_number == 2
    assert stored_chunks[1].source_location == "lines:6-10"
    assert stored_chunks[1].embedding is None

def create_test_document(db_session):
    from uuid import uuid4

    from app.db.models.user import User
    from app.db.models.startup import Startup
    from app.db.models.document import Document

    user = User(
        email=f"constraint-{uuid4()}@example.com",
        password_hash="test-hash",
    )
    db_session.add(user)
    db_session.flush()

    startup = Startup(
        owner_id=user.id,
        name="Database Constraint Test Startup",
    )
    db_session.add(startup)
    db_session.flush()

    document = Document(
        startup_id=startup.id,
        filename="test.txt",
        file_type="txt",
        storage_path="integration/test.txt",
    )
    db_session.add(document)
    db_session.flush()

    return document


def test_postgresql_enforces_unique_document_chunk_index(db_session):
    import pytest

    from sqlalchemy.exc import IntegrityError

    from app.db.models.document_chunk import DocumentChunk

    document = create_test_document(db_session)

    first_chunk = DocumentChunk(
        document_id=document.id,
        chunk_index=0,
        content="First chunk",
    )
    db_session.add(first_chunk)
    db_session.flush()

    # Commit the session's savepoint so the first row remains
    # available within the test's outer transaction.
    db_session.commit()

    duplicate_chunk = DocumentChunk(
        document_id=document.id,
        chunk_index=0,
        content="Duplicate chunk",
    )
    db_session.add(duplicate_chunk)

    with pytest.raises(IntegrityError):
        db_session.flush()

    # Recover the session after the failed flush.
    db_session.rollback()

    stored_chunks = (
        db_session.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document.id)
        .all()
    )

    assert len(stored_chunks) == 1
    assert stored_chunks[0].content == "First chunk"


def test_postgresql_stores_and_retrieves_768_dimension_embedding(
    db_session,
):
    import pytest

    from app.db.models.document_chunk import DocumentChunk

    document = create_test_document(db_session)

    expected_embedding = [
        round(index / 1000, 6)
        for index in range(768)
    ]

    chunk = DocumentChunk(
        document_id=document.id,
        chunk_index=0,
        content="Embedding integration test",
        embedding=expected_embedding,
    )

    db_session.add(chunk)
    db_session.flush()

    db_session.expire(chunk)

    retrieved_chunk = (
        db_session.query(DocumentChunk)
        .filter(DocumentChunk.id == chunk.id)
        .one()
    )

    assert retrieved_chunk.embedding is not None
    assert len(retrieved_chunk.embedding) == 768

    assert retrieved_chunk.embedding == pytest.approx(
        expected_embedding,
        abs=1e-6,
    )

from app.ai.embeddings.base import EmbeddingProvider


class FakeEmbeddingProvider(EmbeddingProvider):
    """Deterministic provider for integration tests; no API calls."""

    def embed_text(self, text: str) -> list[float]:
        seed = sum(ord(character) for character in text)

        return [
            float((seed + index) % 1000) / 1000
            for index in range(768)
        ]


def test_complete_document_processing_pipeline(
    db_session,
    tmp_path,
):
    from uuid import uuid4

    from app.db.models.user import User
    from app.db.models.startup import Startup
    from app.db.models.document import Document
    from app.db.models.document_chunk import DocumentChunk

    from app.services.documents.storage import DocumentStorage
    from app.services.documents.extractors.service import (
        DocumentExtractionService,
    )
    from app.services.documents.chunking import (
        DocumentChunkingService,
    )
    from app.services.document_chunk_persistence_service import (
        DocumentChunkPersistenceService,
    )
    from app.services.document_embedding_service import (
        DocumentEmbeddingService,
    )
    from app.ai.embeddings.service import EmbeddingService
    from app.services.document_processing_service import (
        DocumentProcessingService,
    )

    # 1. Create a real document file in temporary storage.
    storage = DocumentStorage(storage_dir=tmp_path)

    content = (
        "VentureLens integration testing document.\n"
        "The company develops artificial intelligence software.\n"
        "Its revenue model combines subscriptions and enterprise licensing.\n"
        "The company serves customers across multiple industries.\n"
        "Its financial performance has improved over the last year.\n"
        "The business plans to expand into additional markets.\n"
        "Its investment strategy focuses on sustainable growth.\n"
    ).encode("utf-8")

    stored_file = storage.save_file(
        filename="venturelens-report.txt",
        content=content,
    )

    # 2. Create real database ownership records.
    user = User(
        email=f"pipeline-{uuid4()}@example.com",
        password_hash="test-hash",
    )
    db_session.add(user)
    db_session.flush()

    startup = Startup(
        owner_id=user.id,
        name="VentureLens Pipeline Test",
        industry="Artificial Intelligence",
        stage="Seed",
    )
    db_session.add(startup)
    db_session.flush()

    document = Document(
        startup_id=startup.id,
        filename="venturelens-report.txt",
        file_type=stored_file.file_type,
        storage_path=stored_file.storage_path,
        processing_status="pending",
    )
    db_session.add(document)
    db_session.commit()

    document_id = document.id

    # 3. Construct real processing services.
    extraction_service = DocumentExtractionService()

    chunking_service = DocumentChunkingService(
        chunk_size_chars=100,
        overlap_chars=20,
    )

    chunk_persistence_service = (
        DocumentChunkPersistenceService()
    )

    fake_provider = FakeEmbeddingProvider()

    embedding_service = EmbeddingService(
        provider=fake_provider,
        expected_dimension=768,
    )

    document_embedding_service = DocumentEmbeddingService(
        embedding_service=embedding_service,
    )

    processing_service = DocumentProcessingService(
        storage=storage,
        extraction_service=extraction_service,
        chunking_service=chunking_service,
        chunk_persistence_service=chunk_persistence_service,
        embedding_service=document_embedding_service,
    )

    # 4. Execute the complete pipeline.
    result = processing_service.process_document(
        db=db_session,
        document_id=document_id,
    )

    # 5. Verify the processing result.
    assert result.document_id == document_id
    assert result.processing_status == "completed"
    assert result.chunks_persisted > 1
    assert result.embeddings_generated == result.chunks_persisted
    assert result.reused_existing_chunks is False

    # 6. Verify the persisted document status.
    processed_document = (
        db_session.query(Document)
        .filter(Document.id == document_id)
        .one()
    )

    assert processed_document.processing_status == "completed"
    assert processed_document.processing_error is None

    # 7. Read actual chunks back from PostgreSQL.
    chunks = (
        db_session.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.chunk_index)
        .all()
    )

    assert len(chunks) == result.chunks_persisted

    assert [
        chunk.chunk_index for chunk in chunks
    ] == list(range(len(chunks)))

    for chunk in chunks:
        assert chunk.content.strip()
        assert chunk.embedding is not None
        assert len(chunk.embedding) == 768

    # 8. Verify that the original document content was extracted.
    combined_content = " ".join(
        chunk.content for chunk in chunks
    )

    assert "VentureLens integration testing document" in combined_content
    assert "artificial intelligence software" in combined_content

    assert all(
        chunk.source_location is not None
        for chunk in chunks
    )
