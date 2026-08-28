# VentureLens — Detailed Data Model

## 1. Purpose

This document defines the logical relational model that supports startup management, financial data, document intelligence, RAG, agent execution, investment analysis, reporting, and human oversight.

## 2. Core Entities

| Domain | Entities |
|---|---|
| Identity | User |
| Startup | Startup, FinancialRecord |
| Knowledge | Document, DocumentChunk, EvidenceReference |
| Conversation | Conversation, Message |
| Analysis | Analysis, AgentRun, Finding |
| Decision Support | Risk, InvestmentScore, Recommendation, HumanDecision |
| Reporting | Report |
| Audit | AuditLog |

## 3. Main Relationships

```text
User 1 ─────< Startup
Startup 1 ─────< FinancialRecord
Startup 1 ─────< Document
Document 1 ─────< DocumentChunk
Startup 1 ─────< Conversation
Conversation 1 ─────< Message
Startup 1 ─────< Analysis
Analysis 1 ─────< AgentRun
Analysis 1 ─────< Finding
AgentRun 1 ─────< Finding
Finding 1 ─────< EvidenceReference
Analysis 1 ─────< Risk
Analysis 1 ─────< InvestmentScore
Analysis 1 ───── 1 Recommendation
Analysis 1 ───── 0..1 HumanDecision
Analysis 1 ───── 0..1 Report
User 1 ─────< AuditLog
```

## 4. Entity Responsibilities

### User
Stores authenticated analyst accounts and account status.

### Startup
Stores the startup being evaluated and its ownership relationship to the analyst.

### FinancialRecord
Stores period-based structured financial/business metrics. Derived metrics should be calculated deterministically.

### Document
Stores document metadata and processing state. The actual file is stored separately from relational metadata.

### DocumentChunk
Stores retrieval-ready text, source metadata, and vector embeddings. pgvector is the initial vector storage technology.

### Conversation / Message
Stores analyst-to-AI question-answering history scoped to a startup.

### Analysis
Represents one complete due-diligence execution. Completed analyses are retained for history and reproducibility.

### AgentRun
Records execution of an individual specialized agent within an analysis, including status, timing, output metadata, and errors.

### Finding
Stores structured conclusions produced during analysis and links them to the responsible agent run where applicable.

### EvidenceReference
Connects findings to document/chunk/page evidence so important document-based claims can be traced back to source material.

### Risk
Stores identified risks, their category, severity, status, and supporting analysis context.

### InvestmentScore
Stores dimension-level scores, weights, explanations, and analysis association.

### Recommendation
Stores the synthesized investment thesis, strengths, weaknesses, founder questions, and recommendation.

### HumanDecision
Stores the analyst's final decision separately from the AI recommendation.

### Report
Stores generated report content and export metadata.

### AuditLog
Records important user/system actions for auditability and reproducibility.

## 5. Data Integrity Principles

- Foreign keys enforce domain relationships.
- Startup resources must be authorization-scoped.
- Unique constraints should be applied where business identity requires them.
- Timestamps should be stored consistently.
- Completed analyses should not be overwritten by later analyses.
- Document evidence should preserve source identifiers and page/section metadata.
- AI output should not replace deterministic financial calculations.

## 6. Vector Data

`DocumentChunk` will contain an embedding compatible with pgvector. Retrieval will be filtered by authorized startup scope before semantic similarity is evaluated.

## 7. Schema Evolution

Database changes will be managed through Alembic migrations. Schema changes must be reviewed before applying them to shared environments.
