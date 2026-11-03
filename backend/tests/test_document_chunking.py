import pytest

from app.services.documents.chunking import (
    DocumentChunkingError,
    DocumentChunkingService,
)
from app.services.documents.extractors.base import ExtractedSection


def test_short_section_creates_one_chunk():

    service = DocumentChunkingService(
        chunk_size_chars=100,
        overlap_chars=20,
    )

    sections = [
        ExtractedSection(
            text="This is a short startup overview.",
            page_number=1,
            source_location="page:1",
        )
    ]

    chunks = service.chunk_sections(sections)

    assert len(chunks) == 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].content == sections[0].text
    assert chunks[0].page_number == 1
    assert chunks[0].source_location == "page:1"


def test_long_section_is_split_into_multiple_chunks():

    service = DocumentChunkingService(
        chunk_size_chars=100,
        overlap_chars=20,
    )

    text = (
        "This is a sentence about the startup business model. "
        * 15
    )

    sections = [
        ExtractedSection(
            text=text,
            page_number=2,
            source_location="page:2",
        )
    ]

    chunks = service.chunk_sections(sections)

    assert len(chunks) > 1

    assert all(
        len(chunk.content) <= 100
        for chunk in chunks
    )

    assert all(
        chunk.page_number == 2
        for chunk in chunks
    )

    assert all(
        chunk.source_location == "page:2"
        for chunk in chunks
    )


def test_chunk_indexes_are_sequential():

    service = DocumentChunkingService(
        chunk_size_chars=50,
        overlap_chars=10,
    )

    sections = [
        ExtractedSection(
            text="First section. " * 10,
            page_number=1,
            source_location="page:1",
        ),
        ExtractedSection(
            text="Second section. " * 10,
            page_number=2,
            source_location="page:2",
        ),
    ]

    chunks = service.chunk_sections(sections)

    assert [
        chunk.chunk_index for chunk in chunks
    ] == list(range(len(chunks)))


def test_empty_sections_are_ignored():

    service = DocumentChunkingService(
        chunk_size_chars=100,
        overlap_chars=20,
    )

    sections = [
        ExtractedSection(
            text="   ",
            page_number=1,
            source_location="page:1",
        ),
        ExtractedSection(
            text="Valid content.",
            page_number=2,
            source_location="page:2",
        ),
    ]

    chunks = service.chunk_sections(sections)

    assert len(chunks) == 1
    assert chunks[0].content == "Valid content."
    assert chunks[0].page_number == 2


def test_chunk_overlap_preserves_context():

    service = DocumentChunkingService(
        chunk_size_chars=100,
        overlap_chars=20,
    )

    text = " ".join(
        f"sentence{i}."
        for i in range(40)
    )

    sections = [
        ExtractedSection(
            text=text,
            page_number=1,
            source_location="page:1",
        )
    ]

    chunks = service.chunk_sections(sections)

    assert len(chunks) > 1

    assert any(
        set(chunks[index].content.split())
        & set(chunks[index + 1].content.split())
        for index in range(len(chunks) - 1)
    )


def test_chunking_rejects_invalid_overlap():

    with pytest.raises(DocumentChunkingError):

        DocumentChunkingService(
            chunk_size_chars=100,
            overlap_chars=100,
        )


def test_chunking_rejects_negative_overlap():

    with pytest.raises(DocumentChunkingError):

        DocumentChunkingService(
            chunk_size_chars=100,
            overlap_chars=-1,
        )


def test_chunking_rejects_zero_chunk_size():

    with pytest.raises(DocumentChunkingError):

        DocumentChunkingService(
            chunk_size_chars=0,
            overlap_chars=0,
        )


def test_docx_source_location_is_preserved():

    service = DocumentChunkingService(
        chunk_size_chars=100,
        overlap_chars=20,
    )

    sections = [
        ExtractedSection(
            text="Revenue increased during the financial year.",
            page_number=None,
            source_location="table:1/row:2",
        )
    ]

    chunks = service.chunk_sections(sections)

    assert len(chunks) == 1
    assert chunks[0].page_number is None
    assert chunks[0].source_location == "table:1/row:2"