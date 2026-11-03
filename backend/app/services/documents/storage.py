
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from app.core.config import settings
from app.services.documents.validation import validate_document_file


@dataclass(frozen=True)
class StoredDocument:
    storage_path: str
    file_type: str
    mime_type: str
    size_bytes: int


class DocumentStorage:
    def __init__(
        self,
        storage_dir: Path | None = None,
        max_size_bytes: int | None = None,
    ) -> None:
        self.storage_dir = (
            storage_dir
            if storage_dir is not None
            else settings.document_storage_dir
        ).resolve()

        self.max_size_bytes = (
            max_size_bytes
            if max_size_bytes is not None
            else settings.max_upload_size_bytes
        )

    def save_file(
        self,
        filename: str,
        content: bytes,
    ) -> StoredDocument:
        validated = validate_document_file(
            filename=filename,
            content=content,
            max_size_bytes=self.max_size_bytes,
        )

        self.storage_dir.mkdir(parents=True, exist_ok=True)

        stored_filename = f"{uuid4().hex}.{validated.file_type}"
        destination = self.storage_dir / stored_filename

        try:
            with destination.open("xb") as file:
                file.write(content)
                file.flush()
        except Exception:
            destination.unlink(missing_ok=True)
            raise

        return StoredDocument(
            storage_path=str(destination),
            file_type=validated.file_type,
            mime_type=validated.mime_type,
            size_bytes=validated.size_bytes,
        )

    def read_file(self, storage_path: str) -> bytes:
        target = Path(storage_path).resolve()

        if not target.is_relative_to(self.storage_dir):
            raise ValueError(
                "Cannot read a file outside the document storage directory."
            )

        if not target.is_file():
            raise FileNotFoundError(
                f"Stored document does not exist: {target.name}"
            )

        return target.read_bytes()

    
    def delete_file(self, storage_path: str) -> None:
        target = Path(storage_path).resolve()

        if not target.is_relative_to(self.storage_dir):
            raise ValueError(
                "Cannot delete a file outside the document storage directory."
            )

        if target.is_file():
            target.unlink()

