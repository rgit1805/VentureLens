
from io import BytesIO

import pymupdf
from docx import Document

import pytest

from app.services.documents.extractors.base import (
    DocumentExtractionError,
)
from app.services.documents.extractors.service import (
    DocumentExtractionService,
)


def make_pdf() -> bytes:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "VentureLens investment report")

    content = document.tobytes()
    document.close()

    return content


def make_docx() -> bytes:
    document = Document()

    document.add_paragraph("Company overview")
    document.add_paragraph("Revenue increased by 20 percent")

    table = document.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "Year"
    table.cell(0, 1).text = "Revenue"
    table.cell(1, 0).text = "2025"
    table.cell(1, 1).text = "1000000"

    buffer = BytesIO()
    document.save(buffer)

    return buffer.getvalue()


@pytest.fixture
def extraction_service():
    return DocumentExtractionService()


def test_extracts_pdf_text_and_page_number(extraction_service):
    sections = extraction_service.extract(
        "report.pdf",
        make_pdf(),
    )

    assert len(sections) == 1
    assert "VentureLens investment report" in sections[0].text
    assert sections[0].page_number == 1
    assert sections[0].source_location == "page:1"


def test_extracts_docx_paragraphs_and_tables(extraction_service):
    sections = extraction_service.extract(
        "report.docx",
        make_docx(),
    )

    extracted_text = [section.text for section in sections]
    source_locations = [
        section.source_location for section in sections
    ]

    assert "Company overview" in extracted_text
    assert "Revenue increased by 20 percent" in extracted_text
    assert "Year | Revenue" in extracted_text
    assert "2025 | 1000000" in extracted_text

    assert "paragraph:1" in source_locations
    assert "table:1/row:1" in source_locations
    assert all(section.page_number is None for section in sections)


def test_extracts_txt_and_preserves_line_range(extraction_service):
    content = b"Company overview\nFinancial performance\nMarket analysis"

    sections = extraction_service.extract(
        "report.txt",
        content,
    )

    assert len(sections) == 1
    assert "Company overview" in sections[0].text
    assert sections[0].source_location == "lines:1-3"


def test_rejects_pdf_without_extractable_text(extraction_service):
    document = pymupdf.open()
    document.new_page()
    content = document.tobytes()
    document.close()

    with pytest.raises(
        DocumentExtractionError,
        match="No extractable text",
    ):
        extraction_service.extract("empty.pdf", content)


def test_rejects_corrupted_pdf(extraction_service):
    with pytest.raises(DocumentExtractionError):
        extraction_service.extract(
            "corrupted.pdf",
            b"%PDF-1.7 invalid document content",
        )


def test_rejects_empty_docx(extraction_service):
    document = Document()
    buffer = BytesIO()
    document.save(buffer)

    with pytest.raises(
        DocumentExtractionError,
        match="No extractable text",
    ):
        extraction_service.extract(
            "empty.docx",
            buffer.getvalue(),
        )


def test_extracts_txt_without_bom(extraction_service):
    sections = extraction_service.extract(
        "notes.txt",
        b"VentureLens document",
    )

    assert sections[0].text == "VentureLens document"
