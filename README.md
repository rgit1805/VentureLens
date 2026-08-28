# VentureLens

> **VentureLens: An AI-Powered Venture Capital Due Diligence and Investment Analysis Platform**

VentureLens is a full-stack AI-powered decision-support platform designed to assist investment analysts in evaluating startups. It combines structured startup and financial data, due-diligence documents, Retrieval-Augmented Generation (RAG), Machine Learning, specialized AI agents, investment scoring, risk analysis, evidence-backed reasoning, and automated report generation.

> **Important:** VentureLens is a decision-support system. The final investment decision remains with the human investment analyst.

## Problem Statement

Venture capital firms review large numbers of startup opportunities. Evaluating business models, financial health, market potential, competitive position, supporting documents, and risks manually can be time-consuming and difficult to perform consistently.

VentureLens aims to support this process by organizing startup information and combining deterministic analysis, machine learning, retrieval-augmented generation, and specialized AI agents into a structured due-diligence workflow.

## Core Solution

VentureLens provides a virtual AI-assisted due-diligence workflow in which specialized components analyze different aspects of a startup and a final synthesis layer combines the results.

### Core AI Agents

- **Document/RAG Agent** — retrieves and analyzes evidence from uploaded documents.
- **Financial Agent** — analyzes structured financial and business metrics.
- **Market Agent** — analyzes market and competitive information using approved sources.
- **Risk Agent** — identifies, classifies, and prioritizes potential risks.
- **Investment Analyst Agent** — synthesizes findings into an investment thesis and recommendation.

An agent orchestrator coordinates the workflow and preserves execution state, while controlled tools/services prevent unrestricted agent access to application data.

## Major Capabilities

- User authentication and analyst workspace
- Startup profile management
- Structured financial and business data management
- Due-diligence document upload and processing
- Document text extraction, chunking, and embeddings
- Vector-based semantic retrieval using PostgreSQL + pgvector
- RAG-based document question answering with evidence references
- Machine learning prediction and evaluation
- Multi-agent due-diligence analysis
- Investment dimension scoring
- Risk identification and severity classification
- Investment thesis and recommendation generation
- Human decision recording
- Consolidated due-diligence report generation and export
- Analysis dashboard and history
- Auditability and execution tracking

## End-to-End Workflow

```text
User Authentication
        ↓
Startup Management
        ↓
Financial & Business Data
        ↓
Document Upload
        ↓
Document Processing
        ↓
Chunking + Embeddings
        ↓
Vector Search / RAG
        ↓
Due-Diligence Analysis
        ↓
Specialized AI Agents + ML
        ↓
Risk Analysis
        ↓
Investment Scoring
        ↓
Evidence Review
        ↓
Investment Recommendation
        ↓
Due-Diligence Report
        ↓
Dashboard + Analysis History
        ↓
Human Investment Decision
```

## Architecture

VentureLens uses a **modular monolith with supporting services**. The main application boundary is a FastAPI backend, while PostgreSQL/pgvector, Redis/Celery, AI providers, and file storage support specialized workloads.

```text
                         ┌─────────────────────┐
                         │       USER          │
                         │  Investment Analyst │
                         └──────────┬──────────┘
                                    ↓
                         ┌─────────────────────┐
                         │      FRONTEND       │
                         │ Next.js + TypeScript│
                         │    Tailwind CSS     │
                         └──────────┬──────────┘
                                    ↓ REST / HTTPS
                         ┌────────────────────────┐
                         │      FASTAPI API       │
                         │ Auth + Services + API  │
                         └───────────┬────────────┘
                                     │
             ┌───────────────────────┼──────────────────────┐
             ↓                       ↓                      ↓
      ┌─────────────┐       ┌────────────────┐      ┌─────────────┐
      │ PostgreSQL  │       │    AI Layer    │      │  ML Layer   │
      │ + pgvector  │       │ RAG + Agents   │      │ Prediction  │
      └─────────────┘       └───────┬────────┘      └─────────────┘
                                    ↓
                              LLM Provider

                     Background Processing
                              ↓
                       Redis + Celery
```

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js + TypeScript + Tailwind CSS |
| Backend | Python + FastAPI |
| API Validation | Pydantic |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Vector Search | pgvector |
| RAG | LangChain |
| Agent Orchestration | LangGraph |
| LLM | Gemini API (initial provider) |
| Machine Learning | Scikit-learn + Pandas + NumPy |
| Document Processing | PyMuPDF + appropriate parsers |
| Background Jobs | Celery + Redis |
| Testing | Pytest + HTTPX + Playwright |
| Containerization | Docker |
| Version Control | Git + GitHub |

Exact model, embedding, external-data, and production-cloud choices will be finalized through implementation and evaluation.

## Project Documentation

```text
docs/
├── requirements/
│   ├── functional-requirements.md
│   └── Non_Functional-requirements.md
│
├── architecture/
│   ├── system-architecture.md
│   ├── component-architecture.md
│   ├── backend-architecture.md
│   ├── document-processing-architecture.md
│   └── api-design.md
│
├── database/
│   ├── conceptual-data-model.md
│   └── detailed-data-model.md
│
├── decisions/
│   ├── 001-modular-monolith.md
│   ├── 002-postgresql-pgvector.md
│   └── 003-async-processing.md
│
└── implementation/
    └── 01-project-setup.md
```

Documentation is maintained alongside implementation so that requirements, architecture, design decisions, testing, and the final project report remain traceable.

## Development Phases

1. **Requirements & Project Definition** — completed
2. **System Architecture & Technical Design** — in progress / design baseline established
3. **Backend & Database Foundation**
4. **Document Processing & RAG**
5. **Machine Learning Pipeline**
6. **Agentic AI & Orchestration**
7. **Investment Scoring & Risk Intelligence**
8. **Frontend & Dashboard Integration**
9. **Report Generation**
10. **Testing, Evaluation & Deployment**

Implementation follows technical dependencies rather than attempting all features simultaneously.

## Requirements Baseline

VentureLens currently has an approved requirements baseline consisting of:

- **59 Functional Requirements (FR-01 to FR-59)**
- **30 Non-Functional Requirements (NFR-01 to NFR-30)**

These requirements form the baseline for architecture, implementation, testing, and final project reporting.

## Engineering Principles

- Keep API routers thin and business logic in services.
- Keep persistence logic in repositories.
- Separate deterministic calculations from probabilistic AI reasoning.
- Keep agents behind controlled tools and service interfaces.
- Scope startup and document access by authorization.
- Use asynchronous processing for long-running operations.
- Preserve evidence and source traceability for important document-based findings.
- Do not knowingly fabricate citations, pages, statistics, or supporting evidence.
- Keep the final investment decision with the human analyst.
- Maintain documentation as the system evolves.

## Repository Structure

```text
VentureLens/
├── README.md
├── docs/
├── backend/
├── frontend/
├── ai/
├── tests/
├── docker/
├── .env.example
├── .gitignore
└── requirements.txt
```

## Status

**Current Milestone:** Documentation and architecture baseline established.

**Next Implementation Milestone:** FastAPI backend foundation, database connectivity, configuration, logging, and health-check endpoint.