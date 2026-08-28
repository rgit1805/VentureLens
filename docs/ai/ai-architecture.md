# VentureLens — AI Architecture

## 1. Purpose

The AI layer provides RAG, LLM reasoning, specialized agents, controlled tools, and AI evaluation while keeping deterministic application logic outside the model.

## 2. AI Stack

```text
Application Services
        ↓
AI Service Layer
   ├── LLM Service
   ├── Embedding Service
   ├── RAG Service
   ├── Agent Orchestrator
   └── AI Evaluation
        ↓
External AI Provider(s)
```

Initial LLM provider: Gemini API.

The provider is accessed through an abstraction so that the application is not permanently coupled to one vendor.

## 3. AI Responsibilities

### LLM Service

Handles prompt execution, structured output handling, model configuration, and provider errors.

### Embedding Service

Converts document chunks and user queries into vector representations.

### RAG Service

Retrieves relevant evidence, constructs context, invokes the LLM, and preserves source references.

### Agent Orchestrator

Coordinates specialized agents according to the approved due-diligence workflow.

### AI Evaluation

Measures retrieval quality, groundedness, citation correctness, agent behavior, and failure handling.

## 4. AI Reliability Principles

- Evidence should be preferred over unsupported generation.
- Important claims should preserve source references.
- Agents operate only through approved tools.
- Model failures must be surfaced rather than fabricated around.
- Deterministic financial calculations remain outside the LLM.
- Model/provider versions should be recorded where practical for reproducibility.

## 5. Approved Agent Set

The initial system uses five specialized agents:

1. Document/RAG Agent
2. Financial Agent
3. Market Agent
4. Risk Agent
5. Investment Analyst Agent

The exact prompts, tools, state schema, and orchestration graph will be finalized during implementation and evaluation.
