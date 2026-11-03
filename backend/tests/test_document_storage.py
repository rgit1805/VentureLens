
from pathlib import Path

import pytest

from app.services.documents.storage import DocumentStorage
from app.services.documents.validation import DocumentValidationError


def test_saves_file_with_generated_filename(tmp_path: Path):
    storage = DocumentStorage(
        storage_dir=tmp_path,
        max_size_bytes=1024,
    )

    result = storage.save_file(
        "company-report.txt",
        b"VentureLens test document",
    )

    saved_path = Path(result.storage_path)

    assert saved_path.exists()
    assert saved_path.parent == tmp_path.resolve()
    assert saved_path.name != "company-report.txt"
    assert saved_path.read_bytes() == b"VentureLens test document"
    assert result.file_type == "txt"
    assert result.mime_type == "text/plain"
    assert result.size_bytes == len(b"VentureLens test document")


def test_rejects_invalid_file_without_storing_it(tmp_path: Path):
    storage = DocumentStorage(
        storage_dir=tmp_path,
        max_size_bytes=1024,
    )

    with pytest.raises(DocumentValidationError):
        storage.save_file("report.pdf", b"not a PDF")

    assert not list(tmp_path.glob("*"))


def test_delete_removes_file_inside_storage(tmp_path: Path):
    storage = DocumentStorage(
        storage_dir=tmp_path,
        max_size_bytes=1024,
    )

    result = storage.save_file(
        "notes.txt",
        b"temporary document",
    )

    storage.delete_file(result.storage_path)

    assert not Path(result.storage_path).exists()


def test_delete_rejects_path_outside_storage(tmp_path: Path):
    storage_dir = tmp_path / "storage"
    storage_dir.mkdir()

    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("keep this file")

    storage = DocumentStorage(
        storage_dir=storage_dir,
        max_size_bytes=1024,
    )

    with pytest.raises(ValueError, match="outside"):
        storage.delete_file(str(outside_file))

    assert outside_file.exists()


def test_reads_stored_file_successfully(tmp_path: Path):
    storage = DocumentStorage(
        storage_dir=tmp_path,
        max_size_bytes=1024,
    )

    original_content = b"VentureLens document processing test"

    result = storage.save_file(
        "report.txt",
        original_content,
    )

    retrieved_content = storage.read_file(result.storage_path)

    assert retrieved_content == original_content


def test_read_rejects_path_outside_storage(tmp_path: Path):
    storage_dir = tmp_path / "storage"
    storage_dir.mkdir()

    outside_file = tmp_path / "outside.txt"
    outside_file.write_bytes(b"Do not read this file")

    storage = DocumentStorage(
        storage_dir=storage_dir,
        max_size_bytes=1024,
    )

    with pytest.raises(ValueError, match="outside"):
        storage.read_file(str(outside_file))


def test_read_raises_error_for_missing_file(tmp_path: Path):
    storage = DocumentStorage(
        storage_dir=tmp_path,
        max_size_bytes=1024,
    )

    missing_file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError, match="does not exist"):
        storage.read_file(str(missing_file))
