# VentureLens — API Design

## 1. API Style

VentureLens exposes versioned REST APIs through FastAPI.

Base path:

```text
/api/v1
```

## 2. Resource Groups

| Resource | Purpose |
|---|---|
| `/auth` | Registration, login, authentication |
| `/startups` | Startup profiles and lifecycle |
| `/financials` | Structured financial/business data |
| `/documents` | Upload, metadata, processing status |
| `/conversations` | RAG conversations and messages |
| `/analyses` | Due-diligence runs and results |
| `/risks` | Structured risk findings |
| `/reports` | Report generation and retrieval |

## 3. API Principles

- Use resource-oriented URLs and standard HTTP methods.
- Validate requests with Pydantic schemas.
- Return stable response structures and error codes.
- Protect user-specific resources with authentication and authorization.
- Keep long-running operations asynchronous.
- Do not expose internal exceptions, secrets, or database details.

## 4. Typical Flows

### Create Startup

```text
POST /api/v1/startups
        ↓
StartupService
        ↓
StartupRepository
        ↓
PostgreSQL
```

### Upload Document

```text
POST /api/v1/documents
        ↓
Validate + Persist Metadata
        ↓
Queue Processing Job
        ↓
Return Processing Status
```

### Ask RAG Question

```text
POST /api/v1/conversations/{conversation_id}/messages
        ↓
Authorization
        ↓
RAG Service
        ↓
pgvector Retrieval
        ↓
LLM
        ↓
Answer + Evidence
```

### Start Due Diligence

```text
POST /api/v1/analyses
        ↓
Create Analysis
        ↓
Queue Background Workflow
        ↓
Return Analysis ID + Status
```

## 5. Error Response

A consistent error structure will be used:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found."
  }
}
```

## 6. API Documentation

FastAPI's OpenAPI documentation will be used as the implementation-level API reference. Endpoint contracts should be updated when request or response schemas change.
