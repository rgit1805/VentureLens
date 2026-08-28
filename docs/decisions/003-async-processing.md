# ADR-003: Use Asynchronous Processing for Long-Running Work

- **Status:** Accepted
- **Date:** 2026-08-29

## Context

Document extraction, chunking, embedding generation, multi-agent due-diligence analysis, and report generation may take longer than a normal HTTP request should remain open.

## Decision

Use a task queue with **Redis and Celery workers** for long-running background operations.

```text
API Request
   ↓
Create Job / Record Status
   ↓
Redis Queue
   ↓
Celery Worker
   ↓
Processing
   ↓
Persist Result + Status
```

## Consequences

- APIs remain responsive while heavy work runs.
- Processing status can be exposed to the frontend.
- Failures can be recorded and retried in a controlled manner.
- Local development requires the worker infrastructure when asynchronous features are exercised.

## Initial Background Tasks

- Document processing
- Embedding generation
- Complete due-diligence analysis
- Report generation

The exact retry, timeout, concurrency, and monitoring policies will be finalized during implementation.
