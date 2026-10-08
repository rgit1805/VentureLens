# Implementation 01 — Project Setup

## Status

**Implemented — backend and database foundation established; embedding-provider foundation added.**

This document records the actual implementation progress for the initial project setup milestone. It is intentionally limited to work that has been completed and verified.

## Objective

Establish a reproducible development foundation for VentureLens before implementing business functionality.

## Implemented Backend Foundation

The following foundation components are now implemented:

- Python virtual environment
- FastAPI application
- Central configuration using environment variables
- Health-check endpoint
- Structured application logging
- Centralized unhandled exception handling
- API versioning under `/api/v1`
- PostgreSQL connectivity
- SQLAlchemy database session management
- Alembic migration setup
- Automated backend tests

## Implemented Database Foundation

The initial relational schema has been established through SQLAlchemy models and Alembic migrations:

- `users`
- `startups`
- `financial_records`
- `documents`
- `document_chunks`

The database foundation also includes:

- PostgreSQL 18
- PostgreSQL `pgvector` extension
- `document_chunks.embedding` using `vector(768)`
- Composite uniqueness for startup financial records by fiscal year
- Foreign-key relationships between dependent entities

## Implemented Embedding Foundation

The first embedding-layer foundation is now in place:

- Embedding configuration in application settings
- `EmbeddingProvider` application-level interface
- `GeminiEmbeddingProvider` implementation
- Gemini Embedding 2 configuration
- 768-dimensional output configuration
- Dependency injection of the Gemini client for testing
- Empty-input validation
- Embedding-dimension validation
- Mocked provider tests without requiring a live API credential

The selected architecture is documented in **ADR-004: Embedding Model Selection**.

A real Gemini API credential has not been configured yet. Live API generation is therefore intentionally deferred; the provider implementation is currently validated through mocked client tests.

## Verification

The setup milestone has been verified through:

1. Backend application startup and health endpoint verification.
2. Configuration loading verification.
3. PostgreSQL connectivity verification.
4. Alembic migration execution.
5. PostgreSQL/pgvector extension verification.
6. Vector column verification on `document_chunks`.
7. Automated backend test execution.

**Current test result: 7 tests passed.**

The current test suite covers:

- Health endpoint
- Root endpoint
- Embedding configuration
- Embedding provider contract
- Gemini provider success behavior
- Empty-input validation
- Embedding-dimension validation

A Starlette/httpx deprecation warning remains in the test environment; it does not currently cause test failure and is deferred as maintenance work.

## Environment Management

Secrets and environment-specific configuration are supplied through environment variables.

- `backend/.env` is local-only and must not be committed.
- `backend/.env.example` documents required variables without real credentials.
- Gemini API credentials must never be committed or exposed through frontend code.

## Repository Structure

The implemented backend currently follows this direction:

```text
backend/
└── app/
    ├── main.py
    ├── api/
    │   └── v1/
    ├── core/
    ├── db/
    │   └── models/
    └── ai/
        └── embeddings/
```

Additional application modules will be introduced as their corresponding V1 features are implemented.

## Related Architecture

The current embedding architecture is:

```text
Business / Application Code
          ↓
   Embedding Service
          ↓
 Embedding Provider
          ↓
   Gemini / Future Provider
```

The **Embedding Service** is the next implementation component. It will provide the application-facing orchestration layer before embedding generation is connected to document chunks and vector retrieval.

## Next Implementation Step

**Embedding Service**

After the service is implemented and tested, the next dependency sequence is:

```text
Embedding Service
        ↓
Document-chunk embedding generation
        ↓
Vector persistence
        ↓
Similarity retrieval
        ↓
RAG retrieval
        ↓
Grounded document Q&A
```

## Implementation Record

### Key decisions

- PostgreSQL remains the primary relational database.
- pgvector is used instead of introducing a separate vector database for V1.
- Gemini Embedding 2 is the selected V1 embedding provider.
- Embeddings use 768 dimensions.
- Embedding generation is isolated behind a provider abstraction.
- Tests use dependency injection and mocks so development does not depend on a live API credential.

### Related documentation

- `docs/decisions/004-embedding-model-selection.md`
- `docs/database/conceptual-data-model.md`
- `docs/database/detailed-data-model.md`
- `docs/architecture/document-processing-architecture.md`
- `docs/architecture/backend-architecture.md`
