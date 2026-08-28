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
                                    │
                              HTTPS / REST
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │        FASTAPI BACKEND       │
                    │                              │
                    │  API Layer                   │
                    │  Authentication              │
                    │  Business Logic              │
                    │  Validation                  │
                    │  Workflow Control            │
                    └──────────────┬───────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
       ┌─────────────┐     ┌───────────────┐    ┌──────────────┐
       │ PostgreSQL  │     │   AI Layer    │    │   ML Layer   │
       │ + pgvector  │     │               │    │              │
       │             │     │ RAG           │    │ Prediction   │
       │ Application │     │ LLM           │    │ Evaluation   │
       │ Data        │     │ Agents        │    │              │
       └─────────────┘     └───────┬───────┘    └──────────────┘
                                   │
                                   ▼
                           ┌───────────────┐
                           │    Gemini     │
                           │      LLM      │
                           └───────────────┘

                     BACKGROUND PROCESSING
                              │
                              ▼
                       ┌─────────────┐
                       │    Redis    │
                       └──────┬──────┘
                              │
                              ▼
                       ┌─────────────┐
                       │   Celery    │
                       │   Workers   │
                       └─────────────┘

                     EXTERNAL SERVICES
                              │
                              ▼
                 ┌────────────────────────┐
                 │ Market / Web / Other   │
                 │ Approved Data Sources  │
                 └────────────────────────┘