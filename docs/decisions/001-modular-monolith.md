# ADR-001: Use a Modular Monolith for the Initial Backend

- **Status:** Accepted
- **Date:** 2026-08-29

## Context

VentureLens contains multiple domains including authentication, startups, financial data, documents, RAG, agents, ML, scoring, risks, and reports. Splitting these into microservices at the beginning would introduce operational and deployment complexity before independent service boundaries are justified.

## Decision

Implement VentureLens initially as a **modular monolith** using FastAPI. Internal modules will have explicit responsibilities and dependency boundaries.

```text
API
 ↓
Services
 ↓
Repositories / AI / ML
 ↓
Data Stores / External Providers
```

## Consequences

### Positive

- Faster development
- Easier local setup
- Shared transactions and database access
- Clear module boundaries can be tested independently
- Lower operational overhead

### Trade-offs

- Modules share one deployable backend
- Strong internal boundaries must be maintained
- A future service split may require additional infrastructure

## Future Evolution

If a component develops independent scaling, reliability, or deployment requirements, it may be extracted into a separate service after sufficient evidence from the implemented system.
