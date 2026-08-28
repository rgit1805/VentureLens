# VentureLens — System Architecture

## 1. Architecture Overview

VentureLens follows a **modular monolithic application architecture with supporting services**. A single FastAPI backend provides the main application boundary, while PostgreSQL, pgvector, Redis/Celery, and external AI/data providers support specialized workloads.

```text
                         ┌─────────────────────┐
                         │       USER          │
                         │  Investment Analyst │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FRONTEND       │
                         │ Next.js + TypeScript│
                         │    Tailwind CSS     │
                         └──────────┬──────────┘
                                    │ HTTPS / REST
                                    ▼
                    ┌──────────────────────────────┐
                    │        FASTAPI BACKEND       │
                    │                              │
                    │ API + Auth + Services        │
                    │ Workflow + Validation       │
                    └──────────────┬───────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
       ┌─────────────┐     ┌───────────────┐    ┌──────────────┐
       │ PostgreSQL  │     │   AI Layer    │    │   ML Layer   │
       │ + pgvector  │     │ RAG + Agents  │    │ Prediction   │
       └─────────────┘     └───────┬───────┘    └──────────────┘
                                   │
                                   ▼
                           ┌───────────────┐
                           │ LLM Provider  │
                           └───────────────┘

                         Background Processing
                                   │
                              ┌────┴────┐
                              │ Redis   │
                              └────┬────┘
                                   │
                              ┌────▼────┐
                              │ Celery  │
                              │ Workers │
                              └─────────┘
```

## 2. Architectural Layers

### Presentation Layer

- Next.js
- TypeScript
- Tailwind CSS
- User-facing dashboards, forms, document workflows, AI Q&A, reports

The frontend communicates with the backend through REST APIs and does not directly access PostgreSQL, pgvector, or the LLM provider.

### API Layer

FastAPI exposes versioned REST endpoints for authentication, startups, financial data, documents, conversations, analyses, risks, and reports.

### Application / Business Layer

Contains business rules and coordinates core services such as startup management, financial analysis, document management, analysis management, scoring, and reporting.

### AI Layer

Contains LLM integration, RAG, embeddings, agent workflows, tools, and AI evaluation.

### ML Layer

Contains data preparation, feature engineering, model training/evaluation, and runtime prediction.

### Data Layer

- PostgreSQL for relational application data
- pgvector for document embeddings and semantic retrieval metadata

### Infrastructure Layer

- Redis for queue/broker support and selected caching needs
- Celery workers for long-running document, AI, and report-processing tasks
- Docker for reproducible development/deployment

## 3. Core Architectural Principle

VentureLens separates deterministic software logic from probabilistic AI reasoning.

### Deterministic logic

- Financial calculations
- Validation
- Authorization
- Database operations
- Score formulas and thresholds
- Workflow state management

### AI reasoning

- Document interpretation
- Qualitative market analysis
- Risk interpretation
- Investment thesis generation
- Natural-language answers

This separation improves reliability, testability, explainability, and maintainability.

## 4. Core Request Flow

```text
Frontend
  ↓
FastAPI Router
  ↓
Application Service
  ↓
Repository / AI / ML Service
  ↓
Data Store or External Provider
```

Long-running operations are delegated to background workers.

## 5. Due-Diligence Flow

```text
Create Analysis
      ↓
Queue Background Job
      ↓
Agent Orchestrator
      ↓
Document/RAG Agent
      ↓
Financial Agent
      ↓
Market Agent
      ↓
ML Analysis
      ↓
Risk Agent
      ↓
Investment Analyst Agent
      ↓
Investment Scoring Engine
      ↓
Recommendation
      ↓
Report Generation
```

## 6. Architectural Decisions

- Use a modular monolith rather than premature microservices.
- Use PostgreSQL as the primary source of truth.
- Use pgvector initially for vector retrieval.
- Use asynchronous workers for long-running operations.
- Keep AI agents behind controlled service/tool interfaces.
- Preserve evidence references for important document-based conclusions.
- Keep LLM provider integration behind an abstraction.

## 7. Current Technology Baseline

| Layer | Technology |
|---|---|
| Frontend | Next.js + TypeScript + Tailwind CSS |
| Backend | Python + FastAPI |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| Database | PostgreSQL |
| Vector Search | pgvector |
| RAG | LangChain |
| Agent Orchestration | LangGraph |
| LLM | Gemini API (initial provider) |
| ML | Scikit-learn + Pandas + NumPy |
| Document Processing | PyMuPDF + appropriate parsers |
| Background Jobs | Celery + Redis |
| Testing | Pytest + HTTPX + Playwright |
| Containerization | Docker |
| Version Control | Git + GitHub |

Exact model, embedding, external-data, and production-cloud selections remain subject to later evaluation.