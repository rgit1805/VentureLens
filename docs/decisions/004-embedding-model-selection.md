# ADR-004: Embedding Model Selection

**Status:** Accepted
**Date:** 2026-10-05

## 1. Context

VentureLens requires semantic retrieval for its Retrieval-Augmented Generation (RAG) pipeline.

The document-processing workflow extracts uploaded documents into `DocumentChunk` records. These chunks must be converted into numerical vector representations so that relevant evidence can be retrieved using semantic similarity rather than only keyword matching.

The current database architecture uses PostgreSQL with the `pgvector` extension. The `DocumentChunk` model currently stores the extracted text and page information but does not yet store embeddings.

The embedding strategy must therefore consider:

* Retrieval quality
* API cost
* Local development requirements
* GPU availability
* Storage requirements
* Embedding dimensionality
* Integration with PostgreSQL and pgvector
* Future provider replacement
* Implementation complexity
* Suitability for the VentureLens V1 demonstration

## 2. Decision

For VentureLens V1, the project will use:

* **Embedding provider:** Google Gemini API
* **Embedding model:** `gemini-embedding-2`
* **Embedding dimension:** 768
* **Vector database:** PostgreSQL + pgvector
* **Database vector type:** `vector(768)`

The embedding functionality will be implemented behind an application-level provider abstraction so that the embedding model can be replaced in the future without coupling the rest of the RAG system directly to the Gemini API.

## 3. Rationale

### 3.1 No GPU requirement

VentureLens is being developed on a system without a dedicated GPU.

Using the Gemini API means embedding generation does not require local GPU infrastructure. The local machine is responsible for application logic, document processing, database operations, and API communication, while embedding computation is performed by Google's infrastructure.

### 3.2 Suitable for V1 demonstration

The immediate objective is to build a working end-to-end RAG pipeline rather than optimize a large-scale production retrieval infrastructure.

Gemini Embedding 2 provides a practical cloud-based embedding solution while avoiding the additional setup and CPU workload associated with running local embedding models.

### 3.3 Cost

The Gemini API provides a free tier for eligible usage. V1 development and demonstration are expected to remain within the applicable free-tier limits.

The application will not assume unlimited free usage. API quotas and rate limits remain external constraints and must be monitored.

### 3.4 768-dimensional representation

The selected output dimension is 768.

The project does not require the maximum available embedding dimensionality for the V1 demonstration. A 768-dimensional vector provides a practical balance between representation capacity, database storage, and vector-search computation.

A larger dimensionality may be evaluated later if retrieval evaluation demonstrates a meaningful improvement.

### 3.5 PostgreSQL + pgvector

VentureLens already uses PostgreSQL for relational application data.

Using pgvector allows vector embeddings to be stored and searched in the same database rather than introducing a separate vector database for V1.

This reduces infrastructure complexity and avoids synchronization problems between relational records and an independent vector store.

The resulting architecture is:

```
Document
    ↓
DocumentChunk
    ↓
Gemini Embedding 2
    ↓
768-dimensional vector
    ↓
PostgreSQL + pgvector
    ↓
Similarity Search
    ↓
Relevant Evidence
    ↓
Gemini LLM
    ↓
Grounded Analysis
```

### 3.6 Provider abstraction

The RAG system will not directly depend on Gemini-specific implementation details.

An embedding provider abstraction will separate embedding generation from retrieval and persistence.

Conceptually:

```
EmbeddingProvider
    ├── GeminiEmbeddingProvider
    └── Future provider implementations
```

This allows the project to evaluate or replace the embedding provider later without redesigning the complete RAG architecture.

## 4. Alternatives Considered

### Alternative A — Local CPU embedding model

A lightweight Sentence Transformers model such as `all-MiniLM-L6-v2` could run locally without a GPU.

**Advantages:**

* No API cost
* No internet dependency
* Simple for experimentation
* Small vector representation

**Disadvantages:**

* Local CPU inference adds processing time
* Requires downloading and managing the model
* Retrieval quality may differ from the selected cloud model
* Different embedding dimensions would require a different vector schema

This option remains a potential future development/testing provider but is not selected as the primary V1 embedding provider.

### Alternative B — Gemini Embedding 2 with 1536 dimensions

1536 dimensions could provide a larger representation and may be useful for higher-quality retrieval.

However, V1 does not currently justify the additional vector storage and computation because the project has not yet demonstrated that the larger dimensionality provides a meaningful retrieval improvement.

### Alternative C — Gemini Embedding 2 with 3072 dimensions

3072 dimensions provides the maximum selected representation size but introduces substantially greater storage and vector-search requirements.

It is unnecessary for the current V1 demonstration and will not be used unless future evaluation justifies it.

### Alternative D — Separate vector database

A dedicated vector database could be introduced.

However, VentureLens already uses PostgreSQL and the expected V1 dataset size does not justify the additional infrastructure and operational complexity.

PostgreSQL + pgvector is therefore preferred for V1.

## 5. Consequences

### Positive consequences

* No local GPU requirement
* Low infrastructure complexity
* Simple integration with existing PostgreSQL architecture
* Suitable for semantic RAG retrieval
* Low storage requirements at V1 scale
* Embedding provider can be replaced later
* Avoids introducing a separate vector database

### Negative consequences

* Requires network access for embedding generation
* Subject to Gemini API availability and rate limits
* Subject to Gemini pricing/free-tier policy changes
* Embedding quality depends on the selected provider
* The vector dimension becomes part of the database schema

## 6. Data and Security Considerations

Document content sent to an external embedding API must be treated as data leaving the local application environment.

VentureLens must therefore avoid embedding sensitive information unnecessarily and must document the external API dependency.

API credentials must be stored in environment variables and must never be committed to Git.

The embedding API key must not be exposed through frontend code or returned by backend API responses.

## 7. Future Evaluation

The embedding strategy is not considered permanently fixed.

Before a production-scale deployment, VentureLens should evaluate retrieval quality using a domain-specific evaluation dataset containing representative questions and relevant document chunks.

Potential future comparisons include:

* Gemini Embedding 2 at different dimensions
* Local Sentence Transformers models
* Other embedding providers
* Retrieval latency
* Recall@K
* Precision@K
* Citation/evidence relevance
* Cost per processed document
* Storage requirements

Any future model change should be accompanied by an explicit schema/versioning decision because vectors produced by different embedding models should not be mixed within the same retrieval space without a deliberate migration strategy.

## 8. Decision Summary

For VentureLens V1:

**Gemini Embedding 2 + 768 dimensions + PostgreSQL/pgvector**

is accepted as the initial embedding architecture.

The implementation will use a provider abstraction so that the embedding model can be changed or expanded in future versions without tightly coupling the RAG system to a single provider.
