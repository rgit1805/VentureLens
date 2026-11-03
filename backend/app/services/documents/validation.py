
from dataclasses import dataclass
from pathlib import Path
from zipfile import BadZipFile, ZipFile
from io import BytesIO


@dataclass(frozen=True)
class ValidatedDocument:
    original_filename: str
    file_type: str
    mime_type: str
    size_bytes: int


MIME_TYPES = {
    ".pdf": "application/pdf",
    ".docx": (
        "application/vnd.openxmlformats-officedocument."
        "wordprocessingml.document"
    ),
    ".txt": "text/plain",
}


class DocumentValidationError(ValueError):
    """Raised when an uploaded document is invalid."""


def validate_document_file(
    filename: str,
    content: bytes,
    max_size_bytes: int,
) -> ValidatedDocument:
    if not filename or not filename.strip():
        raise DocumentValidationError("Filename is required.")

    if not content:
        raise DocumentValidationError("The uploaded file is empty.")

    if len(content) > max_size_bytes:
        raise DocumentValidationError(
            f"File exceeds the maximum allowed size of "
            f"{max_size_bytes} bytes."
        )

    extension = Path(filename).suffix.lower()

    if extension not in MIME_TYPES:
        raise DocumentValidationError(
            "Unsupported file format. Allowed formats: PDF, DOCX, TXT."
        )

    if extension == ".pdf":
        if b"%PDF-" not in content[:1024]:
            raise DocumentValidationError(
                "The file does not contain a valid PDF signature."
            )

    elif extension == ".docx":
        try:
            with ZipFile(BytesIO(content)) as archive:
                names = set(archive.namelist())

                if (
                    "[Content_Types].xml" not in names
                    or "word/document.xml" not in names
                ):
                    raise DocumentValidationError(
                        "The DOCX file is missing required document parts."
                    )
        except BadZipFile as exc:
            raise DocumentValidationError(
                "The DOCX file is not a valid ZIP-based document."
            ) from exc

    elif extension == ".txt":
        if b"\x00" in content:
            raise DocumentValidationError(
                "The TXT file contains null bytes."
            )

        try:
            content.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise DocumentValidationError(
                "TXT files must use UTF-8 encoding."
            ) from exc

    return ValidatedDocument(
        original_filename=filename,
        file_type=extension.lstrip("."),
        mime_type=MIME_TYPES[extension],
        size_bytes=len(content),
    )
