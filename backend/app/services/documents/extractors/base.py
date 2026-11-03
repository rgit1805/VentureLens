
from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractedSection:
    text: str
    page_number: int | None
    source_location: str


class DocumentExtractionError(Exception):
    """Raised when document text extraction fails."""
