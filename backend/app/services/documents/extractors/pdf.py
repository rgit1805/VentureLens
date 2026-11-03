
import pymupdf

from app.services.documents.extractors.base import (
    DocumentExtractionError,
    ExtractedSection,
)


class PDFExtractor:
    def extract(self, content: bytes) -> list[ExtractedSection]:
        try:
            sections = []

            with pymupdf.open(stream=content, filetype="pdf") as document:
                if document.is_encrypted:
                    raise DocumentExtractionError(
                        "Password-protected PDFs are not supported."
                    )

                for page_index, page in enumerate(document):
                    text = page.get_text("text").strip()

                    if not text:
                        continue

                    sections.append(
                        ExtractedSection(
                            text=text,
                            page_number=page_index + 1,
                            source_location=f"page:{page_index + 1}",
                        )
                    )

            if not sections:
                raise DocumentExtractionError(
                    "No extractable text found in the PDF. "
                    "Scanned PDFs may require OCR."
                )

            return sections

        except DocumentExtractionError:
            raise
        except Exception as exc:
            raise DocumentExtractionError(
                "Unable to extract text from the PDF."
            ) from exc
 