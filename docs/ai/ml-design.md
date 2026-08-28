# VentureLens — ML Design

## 1. Purpose

The ML subsystem provides a validated predictive or classification capability that contributes structured evidence to VentureLens investment analysis.

## 2. Current Status

The exact prediction target and dataset are intentionally **not finalized yet**. They will be selected after comparing suitable public/synthetic datasets, feature availability, business relevance, class balance, and evaluation feasibility.

## 3. Planned Pipeline

```text
Dataset
  ↓
Data Validation
  ↓
Preprocessing
  ↓
Feature Engineering
  ↓
Train / Validation / Test Split
  ↓
Model Training
  ↓
Evaluation
  ↓
Model Selection
  ↓
Persist Model / Metadata
  ↓
Runtime Prediction
```

## 4. ML Principles

- Avoid data leakage.
- Use an appropriate validation strategy.
- Select metrics based on the prediction problem.
- Compare against a simple baseline.
- Record model version and relevant configuration.
- Do not treat model output as guaranteed truth.
- Integrate ML output as one input to investment analysis rather than the sole decision criterion.

## 5. Candidate Evaluation Metrics

For classification:

- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion matrix

For regression:

- MAE
- RMSE
- R²

The final metric set will depend on the selected ML task.

## 6. Runtime Boundary

```text
Analysis Service
      ↓
ML Prediction Service
      ↓
Validated Features
      ↓
Versioned Model
      ↓
Prediction + Metadata
```

The model should not directly access the database or external services.

## 7. Reproducibility

The implementation should record the dataset/model version and relevant preprocessing configuration where practical so that results can be reproduced and evaluated.
