# VentureLens — Component Architecture

## 1. Purpose

This document defines the major logical components of VentureLens and the responsibility of each component.

## 2. Component Overview

```text
VentureLens
│
├── Frontend
│   ├── Authentication UI
│   ├── Analyst Workspace
│   ├── Startup Management
│   ├── Financial Dashboard
│   ├── Document Interface
│   ├── AI Q&A
│   ├── Due-Diligence Analysis
│   ├── Investment Dashboard
│   └── Report Interface
│
├── Backend
│   ├── Authentication
│   ├── Startup Management
│   ├── Financial Management
│   ├── Document Management
│   ├── Conversation Management
│   ├── Analysis Management
│   ├── Risk Management
│   ├── Scoring
│   ├── Recommendation
│   └── Reporting
│
├── AI Layer
│   ├── LLM Service
│   ├── RAG
│   ├── Embeddings
│   ├── Agent Orchestrator
│   └── Agent Tools
│
├── ML Layer
│   ├── Preprocessing
│   ├── Feature Engineering
│   ├── Model Inference
│   └── Evaluation
│
└── Infrastructure
    ├── PostgreSQL
    ├── pgvector
    ├── Redis
    ├── Celery Workers
    └── File Storage
```

## 3. Component Responsibilities

### Frontend

Provides the analyst-facing application and communicates with FastAPI through REST APIs.

### Authentication Component

Handles registration, login, authentication state, authorization, and protected-resource access.

### Startup Component

Manages startup profiles, ownership, lifecycle, and workspace information.

### Financial Component

Stores structured financial/business data and performs deterministic financial calculations.

### Document Component

Handles upload, validation, metadata, storage references, processing status, and document lifecycle.

### Document Processing Component

Extracts, cleans, structures, chunks, embeds, and indexes document content.

### RAG Component

Handles query embedding, retrieval, context construction, grounded generation, and evidence references.

### Agent Component

Contains specialized agents and the orchestrator that coordinates due-diligence analysis.

Initial agents:

- Document/RAG Agent
- Financial Agent
- Market Agent
- Risk Agent
- Investment Analyst Agent

### ML Component

Provides the predictive/classification model and its runtime inference interface. The exact ML task will be finalized after dataset and problem evaluation.

### Scoring Component

Applies the documented investment-scoring methodology and combines dimension-level results into an overall score.

### Risk Component

Stores and manages structured risk findings, severity, evidence, and investigation recommendations.

### Reporting Component

Combines analysis outputs into the final due-diligence report and exportable representation.

## 4. Component Communication Rules

```text
Frontend
   ↓ REST
FastAPI API
   ↓
Application Services
   ├── Repositories → PostgreSQL/pgvector
   ├── AI Services → LLM/RAG/Agents
   └── ML Service → Model Inference
```

Long-running tasks are submitted to background workers.

Agents use controlled tools/services and do not directly manipulate database internals.

## 5. Component Boundaries

- UI concerns remain in the frontend.
- HTTP concerns remain in API routers.
- Business rules remain in application services.
- Persistence remains in repositories.
- AI reasoning remains in AI services.
- Predictive inference remains in ML services.
- Deterministic scoring/calculation remains in application code.

## 6. Integration Principle

Components are designed around clear interfaces so that individual implementations can evolve without forcing changes throughout the system. This is particularly important for LLM providers, embedding models, ML models, and external data services.
