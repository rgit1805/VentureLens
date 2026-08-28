# VentureLens — RAG Design

## 1. Purpose

The RAG subsystem allows VentureLens to answer questions and support analysis using evidence retrieved from startup-specific documents.

## 2. Retrieval Pipeline

```text
User Question
      ↓
Authorization / Startup Scope
      ↓
Query Processing
      ↓
Query Embedding
      ↓
Vector Retrieval
      ↓
Metadata Filtering
      ↓
Relevance Filtering
      ↓
Context Construction
      ↓
LLM Generation
      ↓
Evidence / Citation Mapping
      ↓
Final Answer
```

## 3. Knowledge Source

The initial knowledge source is processed documents stored as document chunks with source metadata and embeddings in PostgreSQL + pgvector.

## 4. Retrieval Controls

Retrieval must respect:

- Authorized startup scope
- Document availability
- Relevant metadata filters
- Configurable top-k retrieval
- Relevance thresholds where appropriate

## 5. Context Construction

Retrieved chunks should be transformed into a structured context containing enough source metadata to allow the generated response to reference the underlying evidence.

## 6. Grounded Generation

The prompt should instruct the model to distinguish between:

- Information supported by retrieved evidence
- Information not available in the provided context

The system should not manufacture document citations or unsupported source details.

## 7. Evidence Model

```text
Answer Claim
    ↓
Evidence Reference
    ↓
Document Chunk
    ↓
Document
    ↓
Page / Section
```

## 8. Conversation History

RAG conversations are scoped to a startup. Conversation history may provide conversational context, but document retrieval remains the source of evidence for document-grounded claims.

## 9. Evaluation

RAG evaluation will include, where practical:

- Retrieval relevance
- Context precision/recall
- Answer groundedness
- Citation correctness
- Failure behavior
- Latency

Chunking, top-k, embedding model, and retrieval thresholds will be evaluated empirically rather than assumed to be optimal.
