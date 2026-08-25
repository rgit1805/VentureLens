                         VENTURELENS
                              │
             ┌────────────────┴────────────────┐
             │                                 │
        Presentation                       Backend
             │                                 │
      Next.js Frontend                FastAPI Application
             │                                 │
             │              ┌──────────────────┼──────────────────┐
             │              │                  │                  │
             │         Core Services        AI Services       ML Services
             │              │                  │                  │
             │        ┌─────┼─────┐      ┌─────┼─────┐           │
             │        │     │     │      │     │     │           │
             │      User  Startup Financial RAG Agents  Scoring  ML
             │
             └────────────────┬──────────────────────────────────┘
                              │
                       Data & Infrastructure
                              │
              ┌───────────────┼────────────────┐
              │               │                │
          PostgreSQL       pgvector          Redis
                                             │
                                           Celery