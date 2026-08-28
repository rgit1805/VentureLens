backend/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── startups.py
│   │       ├── financials.py
│   │       ├── documents.py
│   │       ├── chat.py
│   │       ├── analyses.py
│   │       ├── risks.py
│   │       └── reports.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │
│   ├── db/
│   │   ├── session.py
│   │   └── base.py
│   │
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   │
│   ├── ai/
│   │   ├── llm/
│   │   ├── rag/
│   │   ├── agents/
│   │   ├── tools/
│   │   └── evaluation/
│   │
│   ├── ml/
│   │   ├── preprocessing/
│   │   ├── models/
│   │   ├── training/
│   │   ├── evaluation/
│   │   └── prediction/
│   │
│   ├── documents/
│   ├── analysis/
│   ├── scoring/
│   ├── reports/
│   └── workers/
│
├── tests/
├── alembic/
├── requirements/
├── Dockerfile
└── requirements.txt