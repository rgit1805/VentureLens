
from io import BytesIO
from zipfile import ZipFile

import pytest

from app.services.documents.validation import (
    DocumentValidationError,
    validate_document_file,
)


def make_docx() -> bytes:
    buffer = BytesIO()

    with ZipFile(buffer, "w") as archive:
        archive.writestr(
            "[Content_Types].xml",
            "<Types></Types>",
        )
        archive.writestr(
            "word/document.xml",
            "<document></document>",
        )

    return buffer.getvalue()


def test_accepts_pdf_signature():
    result = validate_document_file(
        "report.pdf",
        b"%PDF-1.7\nsample",
        1024,
    )

    assert result.file_type == "pdf"
    assert result.mime_type == "application/pdf"


def test_accepts_valid_docx_structure():
    result = validate_document_file(
        "report.docx",
        make_docx(),
        1024,
    )

    assert result.file_type == "docx"
    assert result.size_bytes > 0


def test_accepts_utf8_text():
    result = validate_document_file(
        "notes.txt",
        "VentureLens document".encode("utf-8"),
        1024,
    )

    assert result.file_type == "txt"
    assert result.mime_type == "text/plain"


def test_rejects_unsupported_extension():
    with pytest.raises(
        DocumentValidationError,
        match="Unsupported file format",
    ):
        validate_document_file(
            "report.exe",
            b"some content",
            1024,
        )


def test_rejects_extension_content_mismatch():
    with pytest.raises(
        DocumentValidationError,
        match="PDF signature",
    ):
        validate_document_file(
            "report.pdf",
            b"This is not a PDF",
            1024,
        )


def test_rejects_invalid_docx():
    with pytest.raises(DocumentValidationError):
        validate_document_file(
            "report.docx",
            b"not a zip file",
            1024,
        )


def test_rejects_invalid_utf8_text():
    with pytest.raises(
        DocumentValidationError,
        match="UTF-8",
    ):
        validate_document_file(
            "notes.txt",
            b"\xff\xfe\xfa",
            1024,
        )


def test_rejects_empty_file():
    with pytest.raises(
        DocumentValidationError,
        match="empty",
    ):
        validate_document_file(
            "empty.txt",
            b"",
            1024,
        )


def test_rejects_file_over_size_limit():
    with pytest.raises(
        DocumentValidationError,
        match="maximum allowed size",
    ):
        validate_document_file(
            "large.txt",
            b"x" * 11,
            10,
        )
