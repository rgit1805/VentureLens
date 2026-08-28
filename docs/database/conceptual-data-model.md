# VentureLens — Conceptual Data Model

## 1. Purpose

The conceptual data model identifies the major business entities and their relationships before implementation-level database schemas are created.

## 2. Core Entities

```text
User
  │
  └──< Startup
          │
          ├──< FinancialRecord
          ├──< Document
          │       │
          │       └──< DocumentChunk
          │
          ├──< Conversation
          │       └──< Message
          │
          └──< Analysis
                  ├──< Risk
                  ├──< InvestmentScore
                  ├──< Finding / Evidence
                  └── Recommendation
```

## 3. Entity Responsibilities

### User

Represents an authenticated platform user and owns or is authorized to access startup workspaces.

### Startup

Represents the company being evaluated and acts as the primary business scope for financial records, documents, analyses, and related information.

### FinancialRecord

Stores structured financial and business metrics used for deterministic calculations and AI/ML analysis.

### Document

Represents an uploaded due-diligence document and its processing lifecycle.

### DocumentChunk

Represents a retrieval unit extracted from a document, including content, source metadata, and vector embedding.

### Conversation

Represents an analyst's document-grounded Q&A session for a startup.

### Message

Represents an individual user or AI message within a conversation.

### Analysis

Represents one due-diligence analysis run for a startup, including its status, inputs, outputs, and timestamp.

### Risk

Represents a structured risk finding identified during analysis, including category, severity, description, and supporting evidence.

### InvestmentScore

Represents dimension-level and/or overall investment scoring associated with an analysis.

### Finding / Evidence

Represents analytical conclusions and the references that support them. Evidence should connect important conclusions back to source documents or other permitted sources.

### Recommendation

Represents the AI-generated investment thesis/recommendation associated with an analysis while preserving human final decision authority.

## 4. Key Relationships

- One user can have access to multiple startups.
- One startup can have many financial records.
- One startup can have many documents.
- One document can have many chunks.
- One startup can have multiple conversations.
- One conversation contains multiple messages.
- One startup can have multiple analysis runs.
- One analysis can produce multiple risks, scores, findings, evidence references, and one recommendation result.

## 5. Data Isolation Principle

Startup-scoped information must be accessible only to authorized users. This applies to relational records, documents, vector chunks, conversations, and analyses.

## 6. Source of Truth

PostgreSQL is the primary relational source of truth. pgvector stores embeddings associated with document chunks within the same database ecosystem.

## 7. Implementation Note

This conceptual model is intentionally independent of exact table names, indexes, constraints, and column types. Those details belong in `detailed-data-model.md` and database migrations.
