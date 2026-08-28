# VentureLens — Agent Design

## 1. Purpose

The agent system decomposes venture due diligence into specialized responsibilities and combines their outputs into a final investment analysis.

## 2. Approved Agents

| Agent | Responsibility | Primary Inputs |
|---|---|---|
| Document/RAG Agent | Retrieve and interpret documentary evidence | Documents, RAG results |
| Financial Agent | Analyze financial/business metrics | Structured financial data, evidence |
| Market Agent | Analyze market and competitive information | Documents, permitted external data |
| Risk Agent | Identify and classify risks | Findings, financial/market evidence |
| Investment Analyst Agent | Synthesize findings and produce investment analysis | Agent outputs, scores, evidence |

## 3. Orchestration

The initial design uses a stateful workflow orchestrator, with LangGraph as the planned implementation technology.

```text
Analysis Request
      ↓
Initialize Analysis State
      ↓
Document/RAG Agent
      ↓
Financial Agent
      ↓
Market Agent
      ↓
Risk Agent
      ↓
Investment Analyst Agent
      ↓
Scoring / Recommendation
      ↓
Persist Results
```

Execution order may be adjusted when implementation and evaluation show that parallel execution is safe and useful.

## 4. Agent State

The shared analysis state should contain structured information such as:

- Analysis ID
- Startup ID
- Input references
- Retrieved evidence
- Financial findings
- Market findings
- Risk findings
- Scores
- Recommendation inputs
- Agent statuses
- Errors/diagnostics

## 5. Tool Boundary

Agents must use approved tools rather than directly accessing database internals.

```text
Agent
  ↓
Approved Tool
  ↓
Application Service
  ↓
Repository / External Service
```

Examples of tools may include:

- Document retrieval tool
- Financial metrics tool
- Market information tool
- Risk analysis tool
- Evidence lookup tool

## 6. Failure Handling

Each agent run should have a status such as:

```text
PENDING
RUNNING
COMPLETED
FAILED
SKIPPED
```

A failed agent must produce an explicit failure state. The system must not invent a successful result to hide an agent failure.

## 7. Observability

Important agent events should record:

- Analysis ID
- Agent name
- Start/end timestamps
- Status
- Tool calls where appropriate
- Model/provider metadata where practical
- Error information

## 8. Human Oversight

Agent output is decision support. The Investment Analyst Agent may synthesize and recommend, but the final investment decision belongs to the human analyst.

## 9. Implementation Note

Prompts, tool schemas, graph topology, model parameters, and output schemas will be refined through implementation and evaluation. The approved agent responsibilities remain stable unless a documented architecture decision changes them.
