# VentureLens — AI/ML Evaluation Strategy

## 1. Purpose

Evaluation is treated as a first-class engineering activity. AI-generated output will not be considered reliable merely because it appears plausible.

## 2. RAG Evaluation

Evaluate:

- Retrieval relevance
- Retrieval recall/coverage
- Context quality
- Answer groundedness
- Citation/source correctness
- Unsupported-claim behavior
- Latency

## 3. Agent Evaluation

Evaluate:

- Correct agent selection/execution
- Tool-use correctness
- Workflow completion
- Structured output validity
- Failure handling
- Evidence usage
- Consistency across repeated runs where appropriate

## 4. ML Evaluation

The ML model will be evaluated using a held-out test strategy appropriate to the selected task. Metrics will be selected based on business and statistical requirements.

## 5. Evaluation Dataset

Evaluation data should include representative startup/financial/document scenarios and explicit expected outcomes where practical. Synthetic data may supplement public data when real labeled data is unavailable, but its limitations must be documented.

## 6. Regression Evaluation

Important evaluation cases should be retained so that changes to prompts, models, retrieval parameters, agents, or scoring logic can be compared against previous results.

## 7. Human Review

Human review remains important for qualitative outputs such as investment thesis, risks, and recommendations. The analyst's final decision is not replaced by automated evaluation.

## 8. Evaluation Artifacts

Where practical, retain:

- Test inputs
- Expected/ reference outputs
- Retrieved evidence
- Model/provider version
- Evaluation metrics
- Failure examples
- Evaluation timestamp

## 9. Acceptance Principle

A feature is not considered complete solely because the API executes successfully. AI and ML components must also demonstrate acceptable quality against documented evaluation criteria.
