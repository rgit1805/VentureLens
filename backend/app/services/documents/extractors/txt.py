
from app.services.documents.extractors.base import (
    DocumentExtractionError,
    ExtractedSection,
)


class TXTExtractor:
    def extract(self, content: bytes) -> list[ExtractedSection]:
        try:
            text = content.decode("utf-8-sig").strip()

            if not text:
                raise DocumentExtractionError(
                    "The TXT file contains no extractable text."
                )

            lines = text.splitlines()

            return [
                ExtractedSection(
                    text=text,
                    page_number=None,
                    source_location=f"lines:1-{len(lines)}",
                )
            ]

        except UnicodeDecodeError as exc:
            raise DocumentExtractionError(
                "Unable to decode the TXT file as UTF-8."
            ) from exc
