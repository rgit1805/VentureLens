# 8. Non-Functional Requirements

Non-functional requirements define **how the VentureLens system shall operate and the quality attributes it shall maintain**.

## 8.1 Security

| ID | Requirement |
|---|---|
| NFR-01 | The system shall protect user accounts, startup information, documents, and analysis results from unauthorized access. |
| NFR-02 | The system shall enforce data isolation between users and their startup workspaces. |
| NFR-03 | Backend APIs shall authenticate protected requests, authorize resources, validate inputs, and handle invalid requests securely. |

## 8.2 Performance

| ID | Requirement |
|---|---|
| NFR-04 | Normal non-AI API operations should respond within a reasonable time under the expected project workload. |
| NFR-05 | Long-running operations such as document processing, embedding generation, agent execution, and report generation should execute asynchronously where appropriate. |

## 8.3 Reliability & Fault Tolerance

| ID | Requirement |
|---|---|
| NFR-06 | The system shall handle application, database, AI, document-processing, and external-service failures gracefully. |
| NFR-07 | Failure of an individual AI component should not unnecessarily terminate the entire analysis workflow. |

## 8.4 AI Reliability & Explainability

| ID | Requirement |
|---|---|
| NFR-08 | Important AI-generated conclusions should be grounded in available evidence wherever applicable. |
| NFR-09 | The system should provide source traceability for important document-based conclusions. |
| NFR-10 | The system shall not knowingly present fabricated citations, document pages, statistics, or sources as genuine evidence. |
| NFR-11 | Investment recommendations shall provide understandable reasoning and supporting factors. |

## 8.5 Agent Quality & Observability

| ID | Requirement |
|---|---|
| NFR-12 | AI agents shall operate within predefined workflows and approved tools. |
| NFR-13 | Important agent execution events should be recorded for debugging, monitoring, and evaluation. |
| NFR-14 | Agent failures shall be recorded and shall not be replaced with fabricated results. |

## 8.6 Data Integrity & Validation

| ID | Requirement |
|---|---|
| NFR-15 | The system shall maintain consistency between startup, financial, document, analysis, and report data. |
| NFR-16 | The system shall validate structured inputs, file types, file sizes, data types, and required fields. |

## 8.7 Scalability & Architecture

| ID | Requirement |
|---|---|
| NFR-17 | The system shall use a modular architecture with clear boundaries between major components. |
| NFR-18 | The architecture should minimize unnecessary coupling to a single LLM provider. |

Major components should include:

- Frontend
- Backend
- Database
- AI/RAG
- Machine Learning
- Agent System
- External Services

## 8.8 Maintainability

| ID | Requirement |
|---|---|
| NFR-19 | The codebase shall follow clean coding practices, modularity, and separation of concerns. |
| NFR-20 | The project shall maintain documentation for requirements, architecture, database, APIs, AI/ML, testing, and deployment. |
| NFR-21 | The project shall use Git/GitHub with meaningful commits, appropriate branching, `.gitignore`, and secure environment-variable management. |

## 8.9 Testing & Quality

| ID | Requirement |
|---|---|
| NFR-22 | Important backend APIs and workflows shall have automated tests. |
| NFR-23 | RAG and AI components shall be evaluated for retrieval quality, groundedness, citation correctness, and failure handling. |
| NFR-24 | ML models shall be evaluated using an appropriate validation/test dataset. |
| NFR-25 | Critical frontend workflows shall be tested. |

## 8.10 Usability

| ID | Requirement |
|---|---|
| NFR-26 | The interface shall clearly communicate system status, progress, errors, and required user actions. |
| NFR-27 | The application should support common desktop and tablet screen sizes. |

## 8.11 Auditability & Reproducibility

| ID | Requirement |
|---|---|
| NFR-28 | The system shall maintain sufficient information about previous analyses for auditing and review. |
| NFR-29 | Where practical, the system should record relevant model/version, configuration, input version, and analysis timestamp information. |

## 8.12 Human Oversight

| ID | Requirement |
|---|---|
| NFR-30 | VentureLens shall operate as a decision-support system, with the final investment decision remaining with the human analyst. |


# 9. Functional vs Non-Functional Requirement Principle

The project shall follow the following distinction:

> **Functional Requirement = What the system does.**

> **Non-Functional Requirement = How well, securely, reliably, transparently, and maintainably the system performs those functions.**

### Example

**Functional:**

FR-47 — The system shall generate an investment recommendation.

**Non-functional:**

NFR-11 — The recommendation shall provide understandable reasoning and supporting factors.

This distinction shall be maintained throughout the subsequent architecture, development, and testing phases.


# 10. Phase 0 Requirements Status

| Area | Status |
|---|---|
| Project Overview | Defined |
| Problem Statement | Defined |
| Objectives | Defined |
| Target Users | Defined |
| Product Boundary | Defined |
| User Workflow | Defined |
| Functional Requirements | 59 Defined |
| Non-Functional Requirements | 30 Defined |
| Detailed AI/ML Requirements | Pending |
| Detailed Data Requirements | Pending |
| System Architecture | Pending — Phase 1 |

**Note:** All approved functional requirements are part of the intended VentureLens product. They will be implemented according to technical dependencies and development phases rather than being removed from the final scope.