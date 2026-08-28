# VentureLens — Backend Architecture

## 1. Architecture Style

VentureLens uses a **modular monolith** implemented with FastAPI. The backend is organized into clear layers so that API handling, business logic, persistence, AI, and ML responsibilities remain separated.

## 2. Request Flow

```text
HTTP Request
    ↓
API Router
    ↓
Pydantic Schema
    ↓
Application Service
    ↓
Repository / AI / ML Service
    ↓
PostgreSQL / pgvector / External Provider
```

## 3. Layers

### API Layer

Responsible for routes, authentication dependencies, request validation, response schemas, and HTTP error handling. Routers should remain thin.

### Service Layer

Contains application and business logic, permission checks, workflow coordination, deterministic calculations, and coordination between repositories and AI/ML components.

### Repository Layer

Encapsulates database access through SQLAlchemy. Repositories do not contain API or high-level business logic.

### Model Layer

SQLAlchemy models represent persisted entities and relationships.

### Schema Layer

Pydantic models define API input/output contracts. Database models and API schemas remain separate.

### AI/ML Services

AI services provide LLM, RAG, agent, embedding, and evaluation functionality. ML services provide feature processing, model inference, and evaluation functionality.

## 4. Proposed Backend Structure

```text
backend/
└── app/
    ├── main.py
    ├── api/v1/
    ├── core/
    ├── db/
    ├── models/
    ├── schemas/
    ├── repositories/
    ├── services/
    ├── ai/
    │   ├── llm/
    │   ├── rag/
    │   ├── agents/
    │   ├── tools/
    │   └── evaluation/
    ├── ml/
    │   ├── preprocessing/
    │   ├── features/
    │   ├── training/
    │   ├── evaluation/
    │   └── prediction/
    ├── documents/
    ├── analysis/
    ├── scoring/
    ├── reports/
    └── workers/
```

## 5. Core Services

- AuthService
- StartupService
- FinancialService
- DocumentService
- ConversationService
- AnalysisService
- RiskService
- ScoringService
- RecommendationService
- ReportService

## 6. AI Service Boundaries

Agents do not directly manipulate database internals. They access controlled tools/services.

```text
Agent
  ↓
Tool
  ↓
Application Service
  ↓
Repository / External Provider
```

This prevents uncontrolled agent access and makes agent behavior testable.

## 7. Asynchronous Processing

Long-running work such as document processing, embedding generation, complete due-diligence analysis, and report generation is executed asynchronously.

```text
FastAPI
  ↓
Redis / Task Queue
  ↓
Celery Worker
  ↓
Long-running Task
```

## 8. Error Handling

The backend will use standardized application exceptions and centralized exception handlers. Responses should expose stable error codes and safe messages without leaking secrets or internal implementation details.

## 9. Configuration and Security

Configuration is loaded from environment variables through a central settings module. Secrets such as API keys, database credentials, and JWT secrets must never be committed to Git.

Authentication and authorization are enforced before protected startup, document, and analysis resources are accessed.

## 10. Design Principles

1. Keep routers thin.
2. Keep business logic in services.
3. Keep database access in repositories.
4. Keep AI provider integration behind interfaces.
5. Keep deterministic calculations outside the LLM.
6. Isolate startup data by authorization scope.
7. Use asynchronous processing for long-running work.
8. Log important workflow and agent execution events.
