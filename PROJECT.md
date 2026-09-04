# Smithsonian RAG

## 1. Project Overview

**Repository:** `smithsonian-rag`

**Description:** Production-oriented multimodal RAG system for semantic
search and grounded question answering over Smithsonian Open Access
collections.

**Project status:** Planning

The project is a portfolio-grade Retrieval-Augmented Generation (RAG)
system built on public Smithsonian Open Access collection data.

Its primary purpose is to demonstrate senior-level backend engineering
combined with practical, production-oriented AI and RAG engineering
skills.

The project will be developed entirely in English. Source code,
identifiers, comments, commit messages, documentation, architecture
decisions, issues, API descriptions, user-facing text, and repository
content should use English unless a source document itself contains
another language.

------------------------------------------------------------------------

## 2. Project Goals

### Primary goals

-   Demonstrate production-oriented backend engineering.
-   Demonstrate advanced practical knowledge of RAG architectures.
-   Build a real system over a large, heterogeneous public dataset.
-   Support semantic and structured retrieval.
-   Introduce multimodal retrieval where it provides meaningful value.
-   Measure retrieval and answer quality instead of relying only on
    subjective demonstrations.
-   Document architectural decisions and engineering trade-offs.
-   Build a reproducible and testable system.
-   Produce a GitHub repository suitable for a senior backend
    engineering portfolio.
-   Produce a project that can be referenced from LinkedIn, a CV, and
    technical interviews.

### Portfolio positioning

This project must not become a simple:

``` text
documents -> embeddings -> vector database -> LLM
```

tutorial.

The final system should demonstrate relevant engineering concepts such
as:

-   ingestion architecture
-   data provenance
-   document and record normalization
-   chunking strategies
-   metadata modeling
-   dense retrieval
-   sparse retrieval
-   hybrid retrieval
-   metadata filtering
-   reranking
-   query transformation and routing
-   context construction
-   grounded generation
-   citations and source attribution
-   RAG evaluation
-   observability
-   performance engineering
-   failure handling
-   security considerations
-   production-oriented API design

Features should only be added when they contribute to the use case or
demonstrate a meaningful engineering capability.

------------------------------------------------------------------------

## 3. Target Audience

The primary audience is:

-   hiring managers for Senior Backend Engineer roles
-   technical leads and software architects
-   backend and AI engineers conducting technical interviews
-   teams building AI-enabled backend systems
-   technical readers reviewing the GitHub repository

The project should remain understandable to a technically competent
reader who is not a RAG specialist.

------------------------------------------------------------------------

## 4. Data Domain

### Decision D-002 --- Dataset and domain

**Status:** Accepted

**Decision:** Use Smithsonian Open Access collections as the primary
knowledge source.

### Primary data sources

Candidates include:

-   Smithsonian Open Access API
-   Smithsonian Open Access bulk metadata
-   digital assets explicitly suitable for the intended reuse

### Potential data modalities

-   structured JSON metadata
-   textual descriptions
-   2D images
-   IIIF manifests
-   research data
-   selected 3D assets

### Rationale

The Smithsonian Open Access domain provides:

-   a large real-world dataset
-   heterogeneous collection records
-   official programmatic data access
-   structured metadata
-   textual information
-   strong multimodal potential
-   meaningful semantic and structured retrieval problems
-   opportunities for measurable RAG evaluation
-   provenance and rights metadata
-   a visually compelling demonstration domain
-   an application concept that is understandable to non-specialist
    reviewers

### Data licensing constraint

The source-code license of this repository does not apply to Smithsonian
data or digital assets.

The ingestion pipeline must respect the rights and usage metadata
associated with source material. Media assets must only be ingested or
redistributed when their rights designation permits the intended use.

Data provenance and rights information should be retained where
technically appropriate.

------------------------------------------------------------------------

## 5. Product Use Case

**Status:** Open

The concrete user-facing use case has not yet been selected.

The use case must determine which RAG capabilities are genuinely useful
rather than implementing techniques only for demonstration purposes.

Potential directions include:

-   a virtual museum research assistant
-   semantic exploration of Smithsonian collections
-   cross-collection question answering
-   multimodal object discovery
-   historically or semantically related object discovery
-   research-oriented synthesis across collection records

The selected use case should support sufficiently difficult retrieval
problems to justify advanced RAG techniques.

------------------------------------------------------------------------

## 6. Initial High-Level Architecture

The following architecture is conceptual and not yet final.

``` text
                  Smithsonian Data Sources
                           |
                           v
                    Ingestion Pipeline
                           |
                           v
                     Normalization
                           |
                           v
                       Chunking
                           |
                 +---------+---------+
                 |                   |
                 v                   v
           Sparse Index        Dense Embeddings
                 |                   |
                 +---------+---------+
                           |
                           v
                    Hybrid Retrieval
                           |
                           v
                        Reranker
                           |
                           v
                    Context Builder
                           |
                           v
                          LLM
                           |
                           v
              Grounded Answer + Citations
```

Cross-cutting or supporting components may include:

``` text
Evaluation Pipeline
Observability
Persistence
API Layer
Data Provenance
Rights Handling
Configuration
```

This architecture is expected to evolve after the product use case and
initial experiments are defined.

------------------------------------------------------------------------

## 7. Initial Technology Candidates

These are candidates, not final architectural decisions unless
explicitly marked otherwise.

### Language

-   Python 3.12+

### Development environment

-   IntelliJ IDEA with Python support

### Backend

Candidates:

-   FastAPI
-   Pydantic

### Persistence

Candidates:

-   PostgreSQL
-   pgvector
-   SQLAlchemy
-   Alembic

### Testing

Candidate:

-   pytest

### Infrastructure

Candidates:

-   Docker
-   Docker Compose
-   GitHub Actions

### Observability

Candidates:

-   structured logging
-   OpenTelemetry

### AI components

To be decided:

-   LLM provider and model
-   embedding model
-   reranking model
-   sparse retrieval implementation
-   multimodal embedding strategy
-   RAG framework strategy

No technology should be selected solely because it is popular. Decisions
should be based on project requirements, trade-offs, operational
complexity, cost, and portfolio value.

------------------------------------------------------------------------

## 8. Architecture Principles

### 8.1 Avoid unnecessary framework lock-in

Important RAG capabilities should preferably exist behind explicit
application interfaces.

Conceptually:

``` text
Retriever
    |
    +-- DenseRetriever
    +-- SparseRetriever
    +-- HybridRetriever
    +-- RerankingRetriever
```

The exact interfaces will be designed later.

Goals include:

-   replaceable components
-   testability
-   dependency inversion
-   controlled experiments
-   measurable comparison of retrieval strategies
-   reduced coupling to a single AI framework

### 8.2 Production orientation

The project should favor production-relevant engineering over
notebook-only demonstrations.

### 8.3 Evidence over intuition

Retrieval and generation changes should be evaluated where practical.

### 8.4 Incremental complexity

A simple working baseline should be built before advanced RAG techniques
are introduced.

### 8.5 Use-case-driven features

Advanced RAG techniques must solve an identified problem or support a
meaningful experiment.

### 8.6 Scope control

Avoid adding technologies merely to increase the number of technologies
listed in the repository.

------------------------------------------------------------------------

## 9. RAG Capability Roadmap

The roadmap is provisional and may change after the product use case is
selected.

### Phase 1 --- Baseline RAG

Potential scope:

-   Smithsonian data ingestion
-   text extraction
-   normalization
-   metadata modeling
-   chunking
-   embeddings
-   vector retrieval
-   basic query API
-   grounded answer generation
-   citations

### Phase 2 --- Retrieval Engineering

Potential scope:

-   metadata filtering
-   sparse retrieval
-   dense retrieval
-   hybrid retrieval
-   reranking
-   retrieval experiments

### Phase 3 --- Advanced RAG

Candidates:

-   query rewriting
-   multi-query retrieval
-   contextual retrieval
-   parent/child retrieval
-   adaptive retrieval
-   query routing

Only techniques justified by the selected use case and evaluation
results should be implemented.

### Phase 4 --- Multimodal and Structured Retrieval

Candidates:

-   image retrieval
-   image embeddings
-   table or structured metadata retrieval
-   multimodal query handling
-   multimodal context construction
-   selected IIIF integration
-   selected 3D metadata or asset exploration

Multimodality should extend the core RAG system rather than replace
sound retrieval engineering.

### Phase 5 --- Production Engineering

Potential scope:

-   asynchronous processing
-   background ingestion
-   caching
-   retries
-   rate limiting
-   error handling
-   configuration management
-   telemetry
-   performance measurement
-   deployment

------------------------------------------------------------------------

## 10. Evaluation Strategy

Evaluation is a first-class project requirement.

A response that appears correct during a manual demonstration is not
sufficient evidence that the RAG system performs well.

### Retrieval metrics

Candidates include:

-   Recall@K
-   Precision@K
-   Mean Reciprocal Rank (MRR)
-   normalized Discounted Cumulative Gain (nDCG)

### Generation and RAG metrics

Candidates include:

-   context relevance
-   answer relevance
-   faithfulness or groundedness
-   citation correctness
-   citation completeness

The final metric set will be selected after the evaluation dataset and
use case are defined.

### Example experiment progression

``` text
Baseline
Dense retrieval

Experiment A
Dense retrieval + metadata filtering

Experiment B
Hybrid retrieval

Experiment C
Hybrid retrieval + reranking

Experiment D
Hybrid retrieval + reranking + query rewriting
```

Experiments should record both quality and relevant operational costs.

A useful final result should support statements such as:

``` text
Hybrid retrieval with reranking improved Recall@5 from X to Y
on the evaluation set while adding Z ms to p95 retrieval latency.
```

------------------------------------------------------------------------

## 11. Non-Functional Requirements

Concrete targets will be defined later.

Areas to evaluate include:

-   latency
-   throughput
-   retrieval quality
-   indexing time
-   storage requirements
-   token usage
-   LLM cost
-   scalability
-   reproducibility
-   reliability

The project should avoid claiming production readiness without
measurable evidence.

------------------------------------------------------------------------

## 12. Security and Trust

The project should demonstrate awareness of RAG-specific and backend
security concerns.

Topics include:

-   prompt injection through retrieved content
-   malicious or malformed ingested content
-   data provenance
-   rights and licensing metadata
-   unsafe file ingestion
-   input validation
-   secrets management
-   trust boundaries between source data, retrieval, and generation

Specific mitigations will be selected after the ingestion and
application architecture are defined.

------------------------------------------------------------------------

## 13. Repository Structure

Initial target structure:

``` text
smithsonian-rag/
├── README.md
├── PROJECT.md
├── LICENSE
├── docs/
│   ├── architecture/
│   ├── adr/
│   └── evaluation/
├── src/
└── tests/
```

This structure is provisional.

### Documentation responsibilities

`README.md`

-   public-facing project introduction
-   setup and usage
-   architecture summary
-   demonstration
-   key evaluation results

`PROJECT.md`

-   current project state
-   goals
-   roadmap
-   current decisions
-   open questions
-   next step

`docs/adr/`

-   durable records of significant architectural decisions

`docs/evaluation/`

-   evaluation methodology
-   datasets
-   experiment definitions
-   results

`docs/architecture/`

-   detailed architecture documentation and diagrams

Git history preserves previous versions of `PROJECT.md`; obsolete
project states should not be appended indefinitely to this file.

------------------------------------------------------------------------

## 14. Licensing

### Source code

**Decision:** MIT License

The MIT License applies to the source code authored for this repository.

### External data

Smithsonian collection data and digital assets remain subject to their
respective rights and usage designations.

The repository must clearly distinguish between:

-   project source-code licensing
-   external dataset rights
-   external media rights

------------------------------------------------------------------------

## 15. Codex Usage Strategy

Codex usage should be deliberately limited because the available monthly
credit budget is shared with other work.

### ChatGPT should primarily be used for

-   requirements analysis
-   architecture
-   research
-   trade-off analysis
-   design
-   interface design
-   implementation planning
-   debugging analysis
-   code review
-   documentation planning
-   evaluation design

### Codex should primarily be used when repository awareness provides meaningful value

Examples:

-   well-specified implementation tasks
-   changes spanning multiple files
-   repository-aware refactoring
-   test changes across the codebase
-   implementation against already documented interfaces or ADRs

Preferred workflow:

``` text
Problem
   |
   v
Analysis and Design
   |
   v
Architecture Decision
   |
   v
Small, Explicit Implementation Task
   |
   v
Codex, when justified
   |
   v
Review
   |
   v
Next Task
```

Avoid spending Codex credits on broad exploratory prompts that can be
resolved during design.

------------------------------------------------------------------------

## 16. Scope Control

Avoid:

-   feature accumulation for its own sake
-   unnecessary microservices
-   unnecessary infrastructure
-   implementing every known RAG technique
-   excessive UI development at the expense of backend and retrieval
    quality
-   premature cloud optimization
-   premature scaling work
-   adding frameworks without a clear benefit

For every significant feature, ask:

> What problem does this feature solve, and what engineering capability
> does it demonstrate?

------------------------------------------------------------------------

## 17. Decision Log

### D-001 --- Project Purpose

**Status:** Accepted

Build a portfolio project demonstrating Senior Backend Engineering and
applied AI/RAG engineering skills.

### D-002 --- Dataset and Domain

**Status:** Accepted

Use Smithsonian Open Access collections as the primary knowledge domain.

### D-003 --- Project Name

**Status:** Accepted

Repository and project name:

``` text
smithsonian-rag
```

### D-004 --- Project Language

**Status:** Accepted

English is the working language of the entire project.

This includes:

-   source code
-   identifiers
-   comments
-   documentation
-   ADRs
-   issues
-   commit messages
-   API documentation
-   repository descriptions
-   user-facing application text

Exceptions are permitted only when preserving original source material
or when multilingual behavior is an explicit feature being tested.

### D-005 --- Source-Code License

**Status:** Accepted

Use the MIT License for source code authored for the project.

External Smithsonian data and assets are governed separately by their
respective rights metadata.

### D-006 --- RAG Framework Strategy

**Status:** Open

Possible options include:

-   framework-free core components
-   LangChain
-   LlamaIndex
-   a limited combination of custom components and selected framework
    functionality

### D-007 --- Vector Storage

**Status:** Open

PostgreSQL with pgvector is an initial candidate. No decision has been
made.

------------------------------------------------------------------------

## 18. Open Questions

### Product

-   What exact user problem will `smithsonian-rag` solve?
-   Who is the primary user?
-   What should the first demonstration workflow be?

### Dataset

-   Which Smithsonian collections or categories should be included
    initially?
-   How large should the initial corpus be?
-   Which metadata fields are useful for retrieval?
-   Which media types should be included in the first multimodal
    iteration?

### Retrieval

-   Which embedding model should be used?
-   How should sparse retrieval be implemented?
-   Should PostgreSQL/pgvector or a dedicated vector database be used?
-   Which reranker should be evaluated?
-   Is query routing necessary?

### Generation

-   Which LLM should be used?
-   Should inference be local, hosted, or configurable?
-   What citation granularity is required?

### Evaluation

-   How will the ground-truth evaluation dataset be created?
-   Which retrieval metrics should be primary?
-   How will multimodal retrieval be evaluated?

### Architecture

-   Should a RAG framework be used?
-   What should the ingestion architecture look like?
-   What is the appropriate deployment model for the final
    demonstration?

------------------------------------------------------------------------

## 19. Current Status

**Project state:** Planning

### Completed

-   [x] Project motivation defined
-   [x] Portfolio objective defined
-   [x] RAG selected as the core AI architecture
-   [x] Python selected as the implementation language
-   [x] Public-data requirement established
-   [x] Evaluation established as a first-class requirement
-   [x] Codex usage strategy established
-   [x] Living project document established
-   [x] Dataset/domain alternatives investigated
-   [x] Smithsonian Open Access selected
-   [x] Project/repository name selected: `smithsonian-rag`
-   [x] Project language selected: English
-   [x] Source-code license selected: MIT
-   [x] Initial GitHub description selected

### In progress

-   [ ] Define the concrete product use case

### Not started

-   [ ] Define initial dataset scope
-   [ ] Define evaluation approach
-   [ ] Make architecture decisions
-   [ ] Define repository implementation structure
-   [ ] Implement baseline ingestion
-   [ ] Implement baseline retrieval
-   [ ] Implement grounded generation
-   [ ] Build evaluation dataset
-   [ ] Evaluate advanced retrieval
-   [ ] Add multimodal capabilities
-   [ ] Production hardening
-   [ ] Deployment
-   [ ] Final portfolio presentation

------------------------------------------------------------------------

## 20. Next Step

### Step 1.1 --- Product Use Case Selection

Define the concrete user-facing problem that `smithsonian-rag` will
solve.

The next analysis should compare a small number of distinct product
concepts using criteria such as:

1.  RAG depth
2.  retrieval engineering potential
3.  multimodal potential
4.  evaluation feasibility
5.  backend engineering potential
6.  portfolio value
7.  demo clarity
8.  implementation complexity
9.  scope control

Expected output:

``` text
Product concept candidates
          |
          v
Comparison and trade-off analysis
          |
          v
Selected product use case
          |
          v
Use-case decision recorded
          |
          v
Initial dataset scope
```
