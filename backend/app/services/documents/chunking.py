import re
from dataclasses import dataclass

from app.core.config import settings
from app.services.documents.extractors.base import ExtractedSection


@dataclass(frozen=True)
class DocumentChunkData:
    chunk_index: int
    content: str
    page_number: int | None
    source_location: str | None


class DocumentChunkingError(ValueError):
    pass


class DocumentChunkingService:

    def __init__(
        self,
        chunk_size_chars: int | None = None,
        overlap_chars: int | None = None,
    ) -> None:

        self.chunk_size_chars = (
            chunk_size_chars
            if chunk_size_chars is not None
            else settings.document_chunk_size_chars
        )

        self.overlap_chars = (
            overlap_chars
            if overlap_chars is not None
            else settings.document_chunk_overlap_chars
        )

        if self.chunk_size_chars <= 0:
            raise DocumentChunkingError(
                "Chunk size must be greater than zero."
            )

        if self.overlap_chars < 0:
            raise DocumentChunkingError(
                "Chunk overlap cannot be negative."
            )

        if self.overlap_chars >= self.chunk_size_chars:
            raise DocumentChunkingError(
                "Chunk overlap must be smaller than chunk size."
            )

    def chunk_sections(
        self,
        sections: list[ExtractedSection],
    ) -> list[DocumentChunkData]:

        chunks: list[DocumentChunkData] = []

        for section in sections:

            text = section.text.strip()

            if not text:
                continue

            text_chunks = self._split_text(text)

            for content in text_chunks:

                chunks.append(
                    DocumentChunkData(
                        chunk_index=len(chunks),
                        content=content,
                        page_number=section.page_number,
                        source_location=section.source_location,
                    )
                )

        return chunks

    def _split_text(self, text: str) -> list[str]:

        if len(text) <= self.chunk_size_chars:
            return [text]

        chunks: list[str] = []
        start = 0

        while start < len(text):

            end = min(
                start + self.chunk_size_chars,
                len(text),
            )

            if end == len(text):
                final_chunk = text[start:].strip()

                if final_chunk:
                    chunks.append(final_chunk)

                break

            split_end = self._find_split_boundary(
                text=text,
                start=start,
                end=end,
            )

            content = text[start:split_end].strip()

            if content:
                chunks.append(content)

            next_start = max(
                start + 1,
                split_end - self.overlap_chars,
            )

            start = next_start

        return chunks

    def _find_split_boundary(
        self,
        text: str,
        start: int,
        end: int,
    ) -> int:

        window = text[start:end]

        minimum_boundary = int(
            self.chunk_size_chars * 0.65
        )

        boundary_patterns = [
            r"\n\s*\n+",
            r"(?<=[.!?])\s+",
            r"\s+",
        ]

        for pattern in boundary_patterns:

            matches = list(
                re.finditer(pattern, window)
            )

            valid_matches = [
                match
                for match in matches
                if match.end() >= minimum_boundary
            ]

            if valid_matches:

                selected = valid_matches[-1]

                return start + selected.end()

        # No suitable sentence or whitespace boundary:
        # fall back to a hard character limit.
        return end    