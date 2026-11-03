
from io import BytesIO

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

from app.services.documents.extractors.base import (
    DocumentExtractionError,
    ExtractedSection,
)


class DOCXExtractor:
    def extract(self, content: bytes) -> list[ExtractedSection]:
        try:
            document = Document(BytesIO(content))
            sections = []

            paragraph_index = 0
            table_index = 0

            # Iterate over paragraphs and tables in document order.
            for element in document.element.body.iterchildren():

                if element.tag.endswith("}p"):
                    paragraph_index += 1
                    paragraph = Paragraph(element, document)
                    text = paragraph.text.strip()

                    if text:
                        sections.append(
                            ExtractedSection(
                                text=text,
                                page_number=None,
                                source_location=(
                                    f"paragraph:{paragraph_index}"
                                ),
                            )
                        )

                elif element.tag.endswith("}tbl"):
                    table_index += 1
                    table = Table(element, document)

                    for row_index, row in enumerate(table.rows, start=1):
                        cells = [
                            cell.text.strip().replace("\n", " ")
                            for cell in row.cells
                        ]

                        row_text = " | ".join(
                            cell for cell in cells if cell
                        )

                        if row_text:
                            sections.append(
                                ExtractedSection(
                                    text=row_text,
                                    page_number=None,
                                    source_location=(
                                        f"table:{table_index}/row:{row_index}"
                                    ),
                                )
                            )

            if not sections:
                raise DocumentExtractionError(
                    "No extractable text found in the DOCX file."
                )

            return sections

        except DocumentExtractionError:
            raise
        except Exception as exc:
            raise DocumentExtractionError(
                "Unable to extract text from the DOCX file."
            ) from exc
