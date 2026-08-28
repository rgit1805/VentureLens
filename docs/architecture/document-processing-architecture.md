# VentureLens — Document Processing Architecture

## 1. Purpose

This document defines how uploaded due-diligence documents are converted into searchable, evidence-backed knowledge for RAG and AI agents.

## 2. Processing Lifecycle

```text
Upload
  ↓
Validation
  ↓
Secure Storage
  ↓
Document Metadata
  ↓
Queue Processing Job
  ↓
Text Extraction
  ↓
Cleaning / Normalization
  ↓
Document Structuring
  ↓
Chunking
  ↓
Metadata Enrichment
  ↓
Embedding Generation
  ↓
pgvector Storage
  ↓
Processing Complete
  ↓
Available to RAG
```

## 3. Supported Formats — Initial Scope

- PDF
- DOCX
- TXT

The design should allow additional formats to be added later through dedicated extractors.

## 4. Document Metadata

Each document should retain metadata such as:

- Document ID
- Startup ID
- Original filename
- Document type
- Storage reference
- File size
- MIME type
- Processing status
- Upload timestamp
- Processing timestamp

Possible document types include pitch deck, financial report, business plan, market research, and supporting documents.

## 5. Validation

Before processing, the system validates:

- File type and MIME type
- File size
- File integrity where applicable
- Authenticated user access
- Startup ownership/authorization

Invalid files are rejected without entering the processing pipeline.

## 6. Asynchronous Processing

Document extraction, chunking, and embedding generation are potentially long-running operations. They are therefore executed by background workers rather than blocking the upload request.

```text
Upload API
   ↓
Create Document Record
   ↓
Queue Task
   ↓
Worker
   ↓
Process Document
```

## 7. Processing States

Initial states:

```text
UPLOADED → QUEUED → PROCESSING → COMPLETED
                              ↘ FAILED
```

Failed documents should retain safe error information and support controlled retry.

## 8. Text Extraction

The extractor converts supported documents into a normalized internal representation while preserving source information where possible.

Page-level information should be retained for PDFs and equivalent source-location metadata should be retained for other formats where feasible.

## 9. Cleaning and Structuring

Cleaning may normalize whitespace, encoding artifacts, repeated headers/footers, and other extraction noise. Meaningful headings, sections, page numbers, tables or source references should not be discarded unnecessarily.

## 10. Chunking

The structured text is divided into retrieval-sized chunks. Chunk size and overlap are configurable and will be evaluated empirically for retrieval quality.

Each chunk should retain:

- Document ID
- Startup ID
- Chunk index
- Content
- Page/source location
- Section metadata where available

## 11. Embeddings and Vector Storage

Each chunk is converted into an embedding through an embedding-provider abstraction. Initial vector storage is PostgreSQL with pgvector.

```text
Chunk
 ↓
Embedding Model
 ↓
Vector
 ↓
PostgreSQL + pgvector
```

The embedding model should be replaceable without redesigning the document domain model.

## 12. Retrieval Boundary

RAG retrieval must be scoped to data the authenticated analyst is authorized to access.

```text
User
 ↓
Authorized Startup
 ↓
Relevant Documents
 ↓
Relevant Chunks
```

Potential retrieval filters include startup ID, document ID, and document type.

## 13. Evidence Traceability

Every document-grounded finding should be traceable through:

```text
AI Finding
 ↓
Evidence Reference
 ↓
Document Chunk
 ↓
Document
 ↓
Page / Section
```

This supports explainability, auditability, and investigation by the human analyst.

## 14. Reprocessing

Documents should support controlled reprocessing when extraction logic, chunking strategy, or embedding models change. Processing versions should prevent old and new vector representations from being mixed unintentionally.

## 15. Failure Handling

Expected failure classes include:

- Unsupported/corrupt file
- Text extraction failure
- Embedding-provider failure
- Queue/worker failure
- Database failure

The system should mark the processing attempt as failed, log diagnostic information, and expose a safe status to the user.
