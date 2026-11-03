
from app.core.config import settings
from app.services.documents.validation import validate_document_file
from app.services.documents.extractors.base import ExtractedSection
from app.services.documents.extractors.pdf import PDFExtractor
from app.services.documents.extractors.docx import DOCXExtractor
from app.services.documents.extractors.txt import TXTExtractor


class DocumentExtractionService:
    def __init__(self) -> None:
        self.pdf_extractor = PDFExtractor()
        self.docx_extractor = DOCXExtractor()
        self.txt_extractor = TXTExtractor()

    def extract(
        self,
        filename: str,
        content: bytes,
    ) -> list[ExtractedSection]:

        validated = validate_document_file(
            filename=filename,
            content=content,
            max_size_bytes=settings.max_upload_size_bytes,
        )

        if validated.file_type == "pdf":
            return self.pdf_extractor.extract(content)

        if validated.file_type == "docx":
            return self.docx_extractor.extract(content)

        if validated.file_type == "txt":
            return self.txt_extractor.extract(content)

        raise ValueError("Unsupported document type.")
