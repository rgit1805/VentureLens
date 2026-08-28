# ADR-002: Use PostgreSQL and pgvector

- **Status:** Accepted
- **Date:** 2026-08-29

## Context

VentureLens needs relational storage for users, startups, financial records, documents, analyses, risks, scores, recommendations, and audit data. It also requires vector similarity search for RAG.

## Decision

Use **PostgreSQL** as the primary database and **pgvector** for document embeddings and semantic retrieval.

## Rationale

- Strong relational integrity for core application data
- Mature SQL capabilities
- Transactions and constraints
- Vector search can coexist with application data
- Reduces the need for a separate vector database during the initial implementation
- Supports a unified authorization/data-isolation model

## Consequences

Application data and vector retrieval data can be managed within the same database ecosystem. Vector indexing and retrieval performance will be evaluated during the RAG implementation phase.

## Future Evolution

A dedicated vector store may be evaluated later if measured scale or retrieval requirements justify it. Such a change must be supported by evidence rather than assumed architectural complexity.
