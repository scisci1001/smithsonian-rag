# Smithsonian RAG

## 1. Project Overview

**Repository:** `smithsonian-rag`

**Description:** Production-oriented multimodal RAG system for semantic
search and grounded question answering over Smithsonian Open Access
collections.

**Project status:** Corpus Selection Policy v0.2 implemented and evaluated on 200 local records; manual review of all 29 accepted matches completed, with one clear false positive identified

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

**Status:** Accepted

### Smithsonian Collection Investigator

`smithsonian-rag` will be an evidence-driven multimodal RAG system for investigating research questions across Smithsonian Open Access collections.

The system should retrieve relevant collection evidence, aggregate evidence across records and collections where necessary, and produce grounded answers with citations.

The product should go beyond a generic "chat with museum data" experience. It should support direct and metadata-constrained retrieval, comparative retrieval, temporal comparison, multi-document evidence synthesis, cross-collection retrieval, query decomposition, and claim-level grounding.

Generated conclusions must be scoped to the evidence retrieved from the Smithsonian corpus rather than presented as universal historical truth.

### V1 Collection Scope

**Status:** Accepted

The initial corpus will focus on:

- National Air and Space Museum (NASM)
- National Museum of American History (NMAH)

This provides a controlled scope while enabling cross-collection investigations involving aerospace, computing, electronics, technology, material culture, and American history.

The exact record selection, corpus size, usable fields, media availability, and rights constraints remain to be validated during the Dataset Feasibility Spike.


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

-   Python 3.13+

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

## 18. Representative Research Questions

**Status:** Candidate evaluation set

These questions define the retrieval and synthesis capabilities the system should eventually support. They are not yet ground-truth evaluation questions; answerability must first be validated against the actual NASM/NMAH Open Access corpus.

### Level 1 — Direct Evidence Retrieval

**Q01.** What materials were used to construct Apollo Guidance Computer artifacts in the Smithsonian collection?

**Q02.** Who designed and manufactured the Apollo Guidance Computer, and what organizations supplied its key electronic components?

**Q03.** Which Apollo 11 personal equipment objects associated with Buzz Aldrin are represented in the collection?

### Level 2 — Filtered and Structured Retrieval

**Q04.** Which guidance and navigation artifacts in the collection were manufactured by Raytheon for the Apollo program?

**Q05.** What Smithsonian computing artifacts associated with human spaceflight were produced by IBM, Raytheon, or MIT-related organizations?

**Q06.** Which Apollo 11 objects in the collection were flown on the mission, and which comparable objects are unflown examples or test articles?

### Level 3 — Comparative Retrieval

**Q07.** How did onboard computing evolve from the Gemini program to the Apollo program, based on artifacts preserved by the Smithsonian?

**Q08.** How did astronaut-computer interaction change as spacecraft computing systems developed during the Gemini and Apollo programs?

**Q09.** What technological changes in guidance systems can be observed across Smithsonian artifacts from early automated flight through Gemini and Apollo?

### Level 4 — Evidence Synthesis

**Q10.** What evidence in the Smithsonian collections shows how advances in electronics enabled increasingly sophisticated spacecraft guidance systems during the 1960s?

**Q11.** How did redundancy and backup systems contribute to the safety of Apollo lunar missions?

**Q12.** What Smithsonian objects illustrate the transition from mechanical or analog control systems to digital computing in aviation and spaceflight?

### Level 5 — Cross-Collection Investigation

**Q13.** How did the miniaturization of electronics influence both space exploration and consumer technology in the United States during the second half of the twentieth century?

**Q14.** How did portable technologies change the relationship between people and computing from the space age to everyday consumer life?

**Q15.** What Smithsonian collection evidence illustrates how technologies originally developed for specialized scientific, military, or aerospace purposes became part of everyday American life?

### Capability Coverage

The candidate questions collectively exercise exact and semantic retrieval, metadata filtering, entity-aware retrieval, temporal reasoning, multi-document retrieval, hybrid search, reranking, query decomposition, cross-collection retrieval, evidence aggregation, and claim-level citations.

## 19. Open Questions

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

## 20. Dataset Feasibility Spike — Preliminary Findings

**Status:** Completed for initial sample; broader representativeness remains open

Preliminary investigation of the Smithsonian Open Access infrastructure and record model supports continuing with the NASM + NMAH scope.

### Data acquisition

- Prefer the Smithsonian Open Access bulk dataset as the primary ingestion source.
- Use the Open Access API for discovery, sampling, debugging, and targeted record lookup.
- Treat the historical GitHub OpenAccess repository as documentation/reference rather than the primary production data source.

### Observed source-record structure

Smithsonian records expose multiple metadata layers that should be preserved during normalization:

```text
record
├── descriptiveNonRepeating
├── indexedStructured
└── freetext
```

Relevant information may include record identifiers, titles, owning units, data source, dates, people and organizations, places, topics, object types, physical descriptions, identifiers, descriptive notes, media metadata, rights information, and update metadata.

### Architectural implication

The source corpus is not a conventional document-only RAG dataset. The ingestion pipeline must normalize heterogeneous Smithsonian unit metadata into a canonical domain model while preserving the original source record and provenance.

The retrieval design should eventually be able to combine structured metadata constraints with semantic retrieval rather than embedding every field indiscriminately.

### Rights model

Metadata rights and media rights must be modeled separately. A record may expose reusable metadata while associated media has different usage restrictions.

### Update model

The source data is updated over time. V1 does not require incremental ingestion, but the design should avoid preventing a later incremental-update strategy based on record identity and change metadata.

### Preliminary V1 domain slice

The first corpus should focus on a coherent subset spanning computing, electronics, guidance, control, and human-machine interaction from aviation and spaceflight to consumer technology. This connects NASM and NMAH while keeping the initial corpus tractable.

Initial target size for experimentation: approximately **5,000–20,000 records**. This is a working range, not a final requirement.

### Preliminary question feasibility

- Q01–Q03: likely supported
- Q04–Q06: likely supported
- Q07–Q09: likely supported
- Q10–Q12: requires validation of descriptive-text richness
- Q13–Q14: requires validation of cross-collection evidence
- Q15: requires careful evidence validation and may require additional sources

These classifications are provisional until tested against actual NASM and NMAH record samples.

### Remaining work for Step 1.3

- acquire representative NASM and NMAH JSON samples
- perform field-level comparison
- measure field presence and data-quality patterns
- define canonical fields and source mappings
- validate Q01–Q15 against actual records
- finalize the V1 corpus specification

---

## 21. Historical Status (Superseded)

**Project state:** Planning / Dataset Feasibility

### Completed

- [x] Project motivation and portfolio objective defined
- [x] RAG selected as the core AI architecture
- [x] Python selected as the implementation language
- [x] Public-data and evaluation requirements established
- [x] Codex usage strategy and living project document established
- [x] Smithsonian Open Access selected
- [x] Project/repository name selected: `smithsonian-rag`
- [x] Project language selected: English
- [x] Source-code license selected: MIT
- [x] Initial GitHub description selected
- [x] Product use case selected: Smithsonian Collection Investigator
- [x] V1 collection scope selected: NASM + NMAH
- [x] Initial set of 15 representative research questions defined

### In progress

- [ ] Dataset Feasibility Spike — sample-record and field-level analysis

### Not started

- [ ] Validate Q01-Q15 against the actual corpus
- [ ] Define final V1 corpus specification
- [ ] Define evaluation approach and ground truth
- [ ] Make architecture decisions
- [ ] Define repository implementation structure
- [ ] Implement baseline ingestion and retrieval
- [ ] Implement grounded generation
- [ ] Build evaluation dataset
- [ ] Evaluate advanced retrieval
- [ ] Add multimodal capabilities
- [ ] Production hardening and deployment
- [ ] Final portfolio presentation


------------------------------------------------------------------------

## 22. Historical Next Step (Superseded)

### Step 1.3 — Dataset Feasibility Spike: Sample Record Analysis

Inspect the actual Smithsonian Open Access data for NASM and NMAH before designing the ingestion architecture or selecting retrieval infrastructure.

The spike should determine:

1. actual record structure and schema variation
2. useful metadata fields
3. textual content richness
4. identifier structure
5. people and organization fields
6. dates and temporal metadata
7. topics and object types
8. collection and owning-unit metadata
9. media availability
10. rights and reuse metadata
11. data quality and missing-field patterns
12. practical corpus size and acquisition strategy

The candidate research questions Q01-Q15 must then be checked against the available data.

For each question, classify it as:

```text
SUPPORTED
PARTIALLY_SUPPORTED
NOT_SUPPORTED
NEEDS_ADDITIONAL_SOURCE
```

Expected output:

```text
NASM/NMAH sample data
        |
        v
Schema and data-quality analysis
        |
        v
Q01-Q15 feasibility assessment
        |
        v
V1 corpus specification
        |
        v
Architecture and ingestion design
```

No vector database, embedding model, RAG framework, or detailed ingestion architecture should be selected before this feasibility work provides the necessary evidence.

---

## 22A. Dataset Feasibility Checkpoint (Historical)

**Status:** In progress

The initial field-level investigation of real NASM and NMAH records supports the current project direction.

### Confirmed findings

- Smithsonian records require normalization into a canonical domain model rather than direct use of raw JSON as the application model.
- Structured metadata and semantic text representations should be treated separately.
- Metadata rights and media rights must be modeled separately.
- Unit-specific `freetext` labels and identifier conventions require normalization.
- The original source record and provenance should be preserved.
- Some useful retrieval attributes, such as flown/unflown status, may exist only in descriptive text and may later justify derived metadata experiments.
- Q01, Q02, Q06, and Q11 have direct evidence of feasibility in inspected records.
- Q13 and Q14 remain plausible but require stronger cross-collection evidence.
- The canonical domain model remains provisional until it is tested against a larger local sample.

### Provisional Canonical Record v0.1

Conceptual fields:

```text
SmithsonianRecord
├── record_id
├── guid
├── unit_code
├── data_source
├── title
├── description
├── object_types[]
├── topics[]
├── people[]
├── organizations[]
├── dates[]
├── places[]
├── materials[]
├── measurements[]
├── media[]
├── metadata_rights
├── source_url
├── last_updated
└── raw_source
```

This is a domain concept, not yet a final Pydantic model or ADR.

### Representation Strategy

A normalized record should produce at least two representations:

1. **Structured metadata representation** for filtering, faceting, exact retrieval, entity constraints, and query routing.
2. **Semantic text representation** for chunking, embedding, and semantic retrieval.

Raw JSON should not be embedded directly.

### V1 Domain Slice

The current V1 corpus direction is:

> Computing, electronics, guidance, control, and human-machine interaction from aviation and spaceflight to consumer technology.

The initial owning units remain:

- National Air and Space Museum (NASM)
- National Museum of American History (NMAH)

The provisional target size for the first useful corpus is approximately **5,000–20,000 records**, subject to profiling results.

### Next Implementation Step — Step 1.3.2 Local Dataset Sample

This is the next task when work resumes.

Create a small local sample before implementing the production ingestion pipeline:

```text
data/
└── samples/
    ├── nasm/
    │   └── 50–100 records
    └── nmah/
        └── 50–100 records
```

Then implement a small Python dataset-profiler utility to inspect the sample and report metrics such as:

- record count
- title coverage
- description coverage
- date coverage
- name/entity coverage
- topic coverage
- object-type coverage
- materials coverage
- online-media coverage
- metadata-rights distribution
- media-rights distribution
- unique `freetext` field names/labels
- schema differences between NASM and NMAH
- missing-field patterns

### Expected Output

```text
Local NASM/NMAH sample
        |
        v
Dataset profiler
        |
        v
Field coverage and schema analysis
        |
        v
Refined canonical domain model
        |
        v
V1 corpus specification
        |
        v
Ingestion architecture
```

### Implementation Constraint

Do not select or implement a vector database, embedding model, RAG framework, or production ingestion architecture yet.

The next code written for the project should be the minimal Python project structure and dataset-profiler tooling. Codex is not required for this step.

### Resume Point

**Resume at: Step 1.3.2 — Local Dataset Sample and Dataset Profiler.**

---

## 23. Implementation Preparation Checkpoint

**Status:** Accepted

The project is ready to begin its first implementation work, deliberately limited to reproducible sample acquisition and deterministic dataset profiling.

### D-010 — Sample Data Acquisition Strategy

**Status:** Accepted

Do not commit generated NASM/NMAH sample records to the repository. Provide a reproducible acquisition script and exclude generated sample JSON from Git.

Initial target:

- 100 NASM records
- 100 NMAH records

The sample should not be manually curated only for interesting or complete records. It must expose missing fields, schema differences, unusual labels, rights variations, and other data-quality issues.

### D-011 — Dataset Profiler Scope

**Status:** Accepted

The first analysis tool will be a deterministic Python dataset profiler with no LLM, embeddings, vector search, or other AI components.

Initial outputs should include:

- total record count and count by owning unit
- title, description, date, name/entity, topic, object-type, and materials coverage
- online-media coverage and media-type distribution
- metadata-rights and media-rights distributions
- unique `freetext` field names and labels
- NASM/NMAH schema and label differences
- missing-field patterns

The profiler should produce both human-readable console output and machine-readable JSON output.

### D-012 — Initial Dependency Policy

**Status:** Accepted

Keep the first implementation dependency-light. Use the Python standard library where practical.

Initial development dependency:

- pytest

Do not add pandas or other data-processing libraries without a concrete requirement.

### Initial Repository Structure

```text
smithsonian-rag/
├── README.md
├── PROJECT.md
├── LICENSE
├── .gitignore
├── pyproject.toml
├── data/
│   └── samples/
│       └── .gitkeep
├── scripts/
│   └── download_sample.py
├── src/
│   └── smithsonian_rag/
│       ├── __init__.py
│       └── profiling/
│           ├── __init__.py
│           └── dataset_profiler.py
└── tests/
    └── profiling/
        └── test_dataset_profiler.py
```

This structure is intentionally minimal. Do not create speculative packages for APIs, vector stores, embeddings, LLMs, retrieval, or multimodal processing yet.

### Deferred Components

The following remain out of scope for the next implementation step:

- canonical Pydantic domain model
- production normalizer
- embeddings and chunking
- vector database and PostgreSQL
- FastAPI
- LangChain or LlamaIndex
- LLM integration
- multimodal embeddings
- Docker
- production ingestion pipeline

### Next Step — Step 1.3.2 Implementation

Proceed in this order:

1. create the minimal Python project skeleton
2. configure `pyproject.toml`
3. configure `.gitignore` for generated sample data
4. implement reproducible Smithsonian sample acquisition
5. acquire approximately 100 NASM and 100 NMAH records
6. implement the deterministic dataset profiler
7. add unit tests for profiler behavior
8. generate the first dataset profile
9. use measured results to refine the canonical domain model
10. finalize the V1 corpus specification

### Resume Point

**Resume at: creating the minimal Python project skeleton and implementing sample acquisition.**

Codex is not required for this step.

---

## 24. API Validation and Sample Records Checkpoint

**Status:** Completed

The Smithsonian Open Access API has been successfully validated with a real API key and real NASM/NMAH responses.

### API Authentication

Use the local environment variable:

```text
SMITHSONIAN_API_KEY
```

The real key must remain in `.env` and must never be committed. The repository should commit only `.env.example` with a placeholder. AI-provider credentials remain deferred until the LLM and embedding-provider decisions are made.

### Validated API Response

The Smithsonian search endpoint returned HTTP 200. The observed response envelope contains `status`, `responseCode`, and a `response` object with `rows`, `facets`, `rowCount`, and `message`.

Observed search rows contain full EDAN-style records with:

```text
record
├── id
├── title
├── unitCode
├── type
├── url
├── content
│   ├── freetext
│   ├── indexedStructured
│   └── descriptiveNonRepeating
├── hash
├── docSignature
├── timestamp
├── lastTimeUpdated
└── version
```

This suggests that sample acquisition can persist search-result records directly without one detail request per record.

### Validated NASM Sample

Example: `Wright XR-2120, Radial 12 Engine, Cutaway` (`nasm_A19710896000`).

The record demonstrates date, manufacturer, summaries, physical descriptions, place, object type, materials, dimensions, structured metadata, online image media, per-media CC0 usage, multiple image resources, and record-level metadata rights.

### Validated NMAH Sample

Example: `Stromberg Carlson CRT` (`nmah_1347189`).

The record demonstrates a lower-case `maker` label, multiple identifier types (`ID Number`, `catalog number`, `accession number`, `serial number`), multiple object types, measurements, structured metadata, and record-level CC0 metadata usage.

### Confirmed Schema Heterogeneity

Real samples confirm that normalization cannot rely on identical `freetext` labels across owning units.

Example:

```text
NASM: freetext.name[].label = "Manufacturer"
NMAH: freetext.name[].label = "maker"
```

Identifier conventions also vary. The profiler must measure label distributions before normalization rules are finalized.

### Media Consistency Check

The profiler should measure cases where `indexedStructured.online_media_type` indicates media but `descriptiveNonRepeating.online_media.media` is absent.

### D-013 — Raw Sample Persistence

**Status:** Accepted

Persist one raw Smithsonian record per JSON file:

```text
data/samples/
├── nasm/
│   ├── nasm_A19710896000.json
│   └── ...
└── nmah/
    ├── nmah_1347189.json
    └── ...
```

Use `record_ID` for filenames where available. Do not normalize or semantically transform the stored raw JSON.

### D-014 — Search Results as Sample Source

**Status:** Provisionally Accepted

Use paginated search results as the sample source because observed rows already contain full EDAN-style content. Add per-record detail requests only if later profiling proves that required information is missing.

### Next Step — Implement Sample Downloader

Implement:

```text
scripts/download_sample.py
        |
        ├── load local configuration
        ├── call Smithsonian Search API
        ├── retrieve NASM sample
        ├── retrieve NMAH sample
        ├── validate response
        │   ├── successful API response
        │   ├── expected unit
        │   └── record_ID present
        └── persist raw records
             ├── data/samples/nasm/*.json
             └── data/samples/nmah/*.json
```

Initial target:

- 100 NASM records
- 100 NMAH records

The downloader should be deterministic where the API permits it and fail clearly on authentication, HTTP, response-schema, or filesystem errors. Tests should not require live API calls.

### Resume Point

**Resume at: implementation of `scripts/download_sample.py` and its tests.**

After the 200-record sample is available, implement `dataset_profiler.py` and use measured results to refine the canonical domain model.

Codex is still not required for the next step.

---

## 25. Sample Acquisition Implementation Checkpoint

**Status:** Completed

The first implementation milestone has been successfully executed locally.

### Python Runtime

**Decision:** Use Python 3.13 for this project.

The local machine exposes Python 3.13 through the `p313` command. IntelliJ uses the project virtual-environment interpreter directly:

```text
<project-root>/.venv/Scripts/python.exe
```

The project metadata should declare `requires-python = ">=3.13"`.

### Test Status

The downloader unit-test suite is green:

```text
9 passed
```

Tests run successfully from the command line and IntelliJ.

### Local Secret Strategy

Local development uses `.env` with `SMITHSONIAN_API_KEY`. The real `.env` is excluded from Git; `.env.example` contains only a placeholder.

An already-defined process environment variable has priority over the value loaded by `load_dotenv()`. For normal local development, avoid defining the key redundantly in PowerShell or IntelliJ and use `.env` as the single local source.

### Sample Acquisition Result

The downloader successfully retrieved:

- 100 NASM records
- 100 NMAH records

Total: **200 raw Smithsonian records**. Generated records remain excluded from Git.

### D-015 — Working-Directory Independent Defaults

**Status:** Accepted

Default project paths must not depend on the process current working directory.

Observed issue:

- PowerShell from repository root wrote to `data/samples`
- IntelliJ with `scripts` as working directory wrote to `scripts/data/samples`

Repository-controlled defaults must be derived from the script location:

```text
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "samples"
ENV_FILE = PROJECT_ROOT / ".env"
```

Load `.env` explicitly from `ENV_FILE`.

This makes default behavior stable from PowerShell, IntelliJ, tests, and future CI.

An explicitly supplied `--output` path may remain relative to the caller's current working directory.

### IntelliJ Configuration

Recommended configuration:

```text
Python SDK:
<project-root>/.venv/Scripts/python.exe

pytest working directory:
$PROJECT_DIR$

download_sample.py working directory:
$PROJECT_DIR$
```

The code must still behave correctly when the working directory differs.

### Downloader Improvement Backlog

Non-blocking improvement:

- include useful Smithsonian API error-body information such as `API_KEY_INVALID` when HTTP errors occur, without exposing secrets

### Next Step — Dataset Profiler

Implement:

```text
src/smithsonian_rag/profiling/dataset_profiler.py
```

The profiler will analyze the 200 local raw records and produce:

1. human-readable console output
2. machine-readable JSON output

Initial measurements:

- total record count
- records by owning unit
- title coverage
- description coverage
- date coverage
- name/entity coverage
- topic coverage
- object-type coverage
- place coverage
- materials coverage
- declared online-media coverage
- actual `online_media.media` coverage
- declared-media vs actual-media mismatch
- media-type distribution
- metadata-rights distribution
- media-rights distribution
- `freetext` category distribution
- `freetext` label distribution
- identifier-label distribution
- NASM/NMAH schema differences
- missing-field patterns

No normalization rules should be finalized until these measurements are available.

### Resume Point

**Resume at: implementation of `dataset_profiler.py` and its unit tests using the 200-record local NASM/NMAH sample.**

---

## 26. Dataset Profiler and Detail API Investigation — October 2026

**Status:** Completed for the initial 200-record sample

### Implemented tools

- `scripts/download_sample.py`: retrieves raw Smithsonian EDAN search records.
- `src/smithsonian_rag/profiling/dataset_profiler.py`: deterministic field-coverage and schema profiling with JSON and console reports.
- `scripts/inspect_record.py`: compares locally saved search records with the corresponding Content API records.
- Unit tests for downloader, profiler, and inspector logic. The profiler was refactored to reduce cognitive complexity, and its regression tests were retained.

The project uses Python 3.13, IntelliJ IDEA with a project `.venv`, `pytest`, and a locally ignored `.env` for the Smithsonian API key. In the user's PowerShell environment, `p313` invokes Python 3.13; IntelliJ uses `.venv/Scripts/python.exe`.

### Profiler v0.2 — observed sample statistics

The sample comprises 100 NASM and 100 NMAH records, with **0 duplicate record IDs**.

| Metric | NASM | NMAH |
|---|---:|---:|
| Title | 100% | 100% |
| Narrative description | 74% | 10% |
| Physical description | 100% | 97% |
| Any recognized semantic text | 100% | 97% |
| Date | 79% | 28% |
| Name | 89% | 27% |
| Topic | 41% | 5% |
| Object type | 100% | 100% |
| Declared media | 100% | 85% |
| Actual embedded media list | 100% | 0% |
| Declared media without embedded media list | 0% | 85% |

**Interpretation:** NMAH's high semantic-text coverage mostly reflects physical descriptions, not explanatory narrative content. A text-presence check alone is not sufficient for RAG evidence quality. The legacy `description` metric remains for compatibility, while `narrative_description`, `physical_description`, and `total_semantic_text` distinguish content types.

**Sampling limitation:** These are convenience samples taken from ID-sorted API results, not representative random samples. Do not extrapolate percentages to either entire museum collection.

### Schema findings

- NASM and NMAH use different labels for comparable fields, including `Manufacturer` versus `maker` / `manufacturer`.
- NMAH identifier labels include `ID Number`, `catalog number`, `accession number`, and sometimes `serial number`; NASM sample records use `Inventory Number`.
- Rights must be retained separately for record metadata and individual media assets.
- Search-result EDAN records include structured metadata, freetext, and descriptive non-repeating sections.
- Raw source data must be preserved independently of derived structured metadata and semantic text.

### Detail API investigation

The first inspector request returned HTTP 404 when calling the Content API with a bare `record_ID`. Using the search record's EDAN URL identifier (for example `edanmdm:nmah_1203284`) succeeded.

Three NMAH records were compared:

| Record | Extra text entries in detail | Extra media assets in detail | New freetext labels |
|---|---:|---:|---:|
| `nmah_1203284` | 0 | 0 | 0 |
| `nmah_1203285` | 0 | 0 | 0 |
| `nmah_1203286` | 0 | 0 | 0 |

The inspector compares selected summary fields, not a complete raw-JSON diff. All three records declared images but contained zero actual media assets in both search and detail representations.

### D-016 — Detail API Enrichment Strategy

**Status:** Accepted for V1 baseline

**Decision:** Use search-result records as the baseline ingestion input. Do not add a mandatory per-record Content API enrichment request.

**Evidence:** Three targeted NMAH detail requests produced no additional text entries, media assets, or freetext labels under the current comparison.

**Limitation:** This is not evidence that detail requests never add value for other records.

**Revisit if:** Broader, more diverse samples reveal meaningful additional data or a future feature requires it.

### Remaining data risks

- The reason for NMAH's declared-media/embedded-media discrepancy is not yet established.
- The selected 100+100 sample may be biased by ID ordering and subject matter.
- Historical or causal cross-collection questions Q13–Q15 require stronger source evidence.
- A full field-level JSON diff and alternative media sources may be investigated if justified, but are not prerequisites for the baseline model.

## 27. Current Status — Authoritative

**Project state:** Canonical model and normalization completed; Corpus Selection Policy v0.2 implemented and evaluated on 200 local records; manual review of all 29 accepted matches completed, with one clear false positive identified.

### Completed

- [x] Project goal, repository name, use case, language, and MIT source-code license
- [x] NASM + NMAH selected as initial owning units
- [x] 15 candidate research questions drafted
- [x] Minimal Python 3.13 project skeleton and local secret configuration
- [x] Smithsonian Search API authentication validated
- [x] 100 NASM and 100 NMAH raw records downloaded locally
- [x] Dataset profiler implemented, tested, and refactored
- [x] Profiler v0.2 generated and analyzed
- [x] NMAH media discrepancy identified and quantified in the sample
- [x] Content API identifier issue diagnosed and corrected
- [x] Three NMAH search/detail comparisons completed
- [x] D-016 baseline detail-enrichment decision recorded
- [x] D-019 Corpus Selection Policy v0.2 implemented with matched-term provenance and positive regression tests
- [x] Selection policy v0.2 evaluated on all 200 local NASM/NMAH records

### In progress / open

- [x] Accept canonical `SmithsonianRecord` v0.1 conceptual schema
- [x] Implement and validate unit-specific NASM/NMAH mapping rules
- [x] Define narrative versus physical evidence representations
- [x] Complete manual precision review of all 29 v0.2 matches; one clear false positive and unresolved scope questions documented
- [ ] Review plausible v0.2 false negatives; then finalize a coherent V1 corpus slice and sampling strategy
- [ ] Validate the representative research questions against the selected corpus
- [ ] Investigate NMAH media access further only if required for V1
- [ ] Select embedding model, LLM, retrieval storage, and RAG framework based on requirements

### Not started

- [ ] Production normalizer and ingestion pipeline
- [ ] Chunking, indexing, retrieval, and grounded generation
- [ ] Ground-truth evaluation dataset and retrieval experiments
- [ ] Multimodal retrieval, operational hardening, and deployment

## 28. Step 1.4 — Canonical Domain Model and V1 Corpus Selection

**Status:** Canonical model and normalization completed; Corpus Selection Policy v0.2 implemented and evaluated on the existing 200-record sample. Manual precision review of all 29 accepted matches is complete; corpus criteria remain provisional pending scope decisions and false-negative review.

The canonical record model preserves source identity, provenance, structured metadata, distinct narrative and physical text, record-level rights, and per-media rights. The initial V1 domain spans computing, electronics, guidance, control, and human-machine interaction across NASM and NMAH.

The deterministic policy and its first evaluation are recorded in Section 31. The measured 4% selection rate applies only to the current convenience sample; it does not establish the final corpus size or representativeness.

Embeddings, vector storage, and LLM-based enrichment remain deferred until the selected corpus and research-question coverage have been reviewed.


---

## 29. Canonical Domain Model v0.1 — Accepted Decision

### D-017 — Canonical Domain Model

**Status:** Accepted and implemented (v0.1)

**Decision:** Represent heterogeneous NASM and NMAH EDAN records using explicit Pydantic domain models and deterministic, unit-aware normalization. Preserve source identity, provenance, original source field labels, and separate narrative from physical evidence. No LLM extraction in the baseline normalizer.

### Accepted canonical fields

| Field | Type | Requirement |
|---|---|---|
| `record_id` | `str` | Required non-empty |
| `unit_code` | `str` | Required non-empty |
| `title` | `str` | Required non-empty |
| `guid` | `str \| None` | Optional |
| `source_url` | `str \| None` | Optional; citation link where available |
| `narrative_texts` | `list[TextEntry]` | Always present, possibly empty |
| `physical_descriptions` | `list[TextEntry]` | Always present, possibly empty |
| `object_types` | `list[str]` | Always present, possibly empty |
| `topics` | `list[str]` | Always present, possibly empty |
| `entities` | `list[Entity]` | Always present, possibly empty |
| `dates` | `list[DateValue]` | Always present, possibly empty |
| `places` | `list[str]` | Always present, possibly empty |
| `identifiers` | `list[Identifier]` | Always present, possibly empty |
| `media` | `list[MediaAsset]` | Always present, possibly empty |
| `metadata_rights` | `RightsInfo` | Required; unknown status must be representable |
| `source_metadata` | `SourceMetadata` | Required; provenance and change information |

`TextEntry` preserves `category`, `label`, and `content`. Normalization retains distinct identifiers and entity roles, avoids inventing exact dates from approximate date strings, and models media usage rights separately from metadata rights.

The original raw EDAN record remains available in the raw-data storage layer rather than being copied into every canonical domain object. Structured metadata and semantic text are separate downstream representations.

### Implementation conventions

- Python 3.13; IntelliJ uses the local `.venv` interpreter. The `p313` command selects Python 3.13 in the user's PowerShell environment.
- Add Pydantic as an explicit dependency when implementing the model.
- Place models under `src/smithsonian_rag/domain/` and normalization under `src/smithsonian_rag/normalization/`.
- Keep normalization deterministic and testable with offline NASM/NMAH fixtures.
- Keep all repository code, tests, comments, documentation, and user-facing text in English.
- Do not commit `.env` or downloaded raw samples.

### Implementation outcome

The accepted Pydantic domain models and deterministic NASM/NMAH normalizers were implemented and validated in Steps 1.4.1 and 1.4.2. The next project work is the selection-quality review described in Section 31, followed by research-question coverage analysis.

**Not yet decided:** final corpus inclusion rules and size, embedding/LLM providers, vector storage, and RAG framework.


---

## 30. Canonical Normalization Implementation and Validation

**Status:** Completed — Step 1.4.1 and Step 1.4.2

### Implemented

- Pydantic-based `SmithsonianRecord` and supporting domain models.
- Deterministic, unit-aware NASM and NMAH normalizers.
- Offline unit tests for canonical models and normalization.
- A batch normalization validator under `src/smithsonian_rag/validation/normalization_validator.py`, with offline tests.
- Machine-readable validation report at `build/normalization-validation.json` (generated locally, not committed).

A minor JSON serialization defect in the validation CLI was corrected: the output now ends with a real newline character (`"\\n"` in Python source), rather than a literal backslash followed by `n`. The report was regenerated successfully.

### Validation results — 200-record local sample

| Metric | Result |
|---|---:|
| Total input records | 200 |
| Successfully normalized | 200 |
| Failed normalization | 0 |
| NASM normalized | 100 / 100 |
| NMAH normalized | 100 / 100 |

Canonical field presence by owning unit:

| Canonical field | NASM | NMAH |
|---|---:|---:|
| Narrative text | 74 / 100 | 10 / 100 |
| Physical descriptions | 100 / 100 | 97 / 100 |
| Entities | 89 / 100 | 27 / 100 |
| Dates | 79 / 100 | 28 / 100 |
| Topics | 41 / 100 | 5 / 100 |
| Media assets | 100 / 100 | 0 / 100 |

**Interpretation:** All 200 sampled records satisfy the implemented normalization contract. The original differences in narrative richness and media availability persist in the canonical representation. This is a successful integration check, not proof of semantic correctness for every mapped field or representativeness of the full museum collections.

### D-018 — Normalization Validation Gate

**Status:** Accepted for the current baseline

Use offline unit tests and a batch validation report as separate quality checks:

- Unit tests verify deterministic mapping and model contracts.
- Batch validation measures conversion success, failure diagnostics, and canonical field coverage.
- Do not silently drop invalid records; report their IDs, units, and validation errors.
- Do not treat normalization success alone as a measure of retrieval usefulness.

The 200-record convenience sample has **zero failures**, but the gate must be reassessed when corpus selection expands to new records and subject areas.

## 31. Step 1.4.3 — Corpus Selection Policy v0.2 and Initial Evaluation

**Status:** Policy v0.2 implemented and evaluated on the 200-record convenience sample. Manual review of all 29 accepted matches is complete; final corpus criteria remain provisional pending scope decisions and false-negative review.

### D-019 — Corpus Selection Policy

**Status:** Implemented; v0.2 is the current baseline for evaluation.

The policy is deterministic, versioned, and unit-aware. It applies field-specific terms to the canonical title, topics, object types, narrative texts, physical descriptions, and entity names. NASM and NMAH use the same vocabulary and have separate metrics. Decisions record the policy version, matched domains, exact matched term and canonical field, evidence class, and reason codes.

Evidence classes:

- **A — Narrative evidence:** at least one non-blank canonical narrative text.
- **B — Structured evidence:** no narrative text, but at least one usable physical description or structured metadata value.
- **C — Insufficient evidence:** neither narrative nor usable structured evidence is present.

A record is accepted only when it matches a domain and has A or B evidence. There is no arbitrary text-length threshold and no LLM-based classification.

### Policy refinement from manual sample review

The review of the eight v0.1 matches found no clear false positives, while inspection of excluded records identified likely missed aviation and electronics evidence. The vocabulary was refined to cover:

- Autopilot spellings `autopilot`, `automatic pilot`, and `auto pilot`.
- Directional gyros, gyroscopes, radio and magnetic compasses, navigational instruments, flight instruments, inclinometers, accelerometers, drift meters, and astrodromes in suitable fields.
- Radar, communication systems, receivers, transmitters, and antennas in suitable fields.
- Instrument panels as cockpit and flight-test evidence.
- Mechanical typewriters as HMI artifacts. This is an explicit scope choice: historic mechanical keyboards are included in the project's human-machine-interaction and consumer-technology coverage.

The policy intentionally does not match `stabilizer` by itself because the sample uses it for ordinary aircraft structure. A generic `Navigation` topic by itself is not sufficient; this avoids selecting an unrelated Galileo pendulum clock. Generic `control`, `display`, and `radio` terms are not used by themselves.

The selection result schema now stores `matched_terms` with the domain, field, and matched phrase to support auditing.

### Evaluation — 200 local records

The 200 source records were reprocessed with policy v0.2. The machine-readable report is generated under `build/` and is not committed with the raw sample data.

| Metric | v0.1 | v0.2 |
|---|---:|---:|
| Input records | 200 | 200 |
| Domain matched / accepted | 8 | 29 |
| Accepted with narrative evidence (A) | 8 | 17 |
| Accepted with structured evidence (B) | 0 | 12 |
| Excluded as insufficient evidence (C) | 0 | 0 |
| Excluded as out of domain | 192 | 171 |
| Selection rate | 4.0% | 14.5% |

| Owning unit | Input | Accepted A | Accepted B | Accepted | Selection rate |
|---|---:|---:|---:|---:|---:|
| NASM | 100 | 14 | 11 | 25 | 25.0% |
| NMAH | 100 | 3 | 1 | 4 | 4.0% |

Accepted domain counts overlap where a record matches multiple domains: guidance 14, control 9, electronics 8, and human-machine interaction 4. No computing matches were found.

### Interpretation and limitations

The increase from 8 to 29 selected records confirms that v0.1 missed terms represented in the current sample, especially autopilot variants, navigation instruments, radio equipment, radar, and antennas. The updated policy also selects structured-only evidence and reports the precise matching field and term.

All reported rates describe this existing 100+100 convenience sample only. It was assembled for data profiling and is not established as representative of the technology domain or of the full Smithsonian collections. Do not project the 14.5% rate to the final corpus size.

### Manual review of the 29 v0.2 matches

All 29 accepted records were inspected individually against their source metadata and descriptions. The review found one clear false positive and several records whose inclusion depends on how contextual aircraft records are treated in the V1 corpus. This is a qualitative review of selected records only; it does not establish recall or false-negative rates.

- **Clear false positive — `nasm_A19360009000`, “Flare, Drift, NC-3”.** The record was selected through the object type `Navigational instruments`, but its description identifies the flare as a signal used to show rescuers the aircraft's position. The taxonomy label is not supported by the artifact's function in this record. Exclude this record and refine the generic object-type match so a navigational-instrument label alone cannot select this kind of signaling device. Add it as a negative regression case when the policy is revised.
- **Classification review — `nasm_A19480159000`, G-Meter / Accelerometer.** The artifact is a flight instrument and appears relevant to the scope, but the current `guidance` domain label may be inaccurate. Review the domain vocabulary or allow an appropriate control/instrumentation classification; do not treat this as a relevance false positive.
- **Context-dependent records.** Several accepted records describe whole aircraft or aircraft-level systems, with the relevant evidence appearing in contextual descriptions: Langley Aerodrome (control system), Douglas World Cruiser (flight instrumentation), Lockheed Vega (autopilot/radio compass), Bell XP-59A (instrument panel), Piper PA-12 (radio/navigation equipment), Fowler-Gage (control system), Bell X-1 (flight-test instrumentation), and P-61 (radar). Their evidence is relevant, but whether to retain them depends on whether V1 includes contextual platform records as well as standalone technology artifacts. Make that scope decision before freezing the corpus slice.
- **HMI boundary.** The mechanical typewriter matches remain consistent with the explicit project decision to include historic typewriters as HMI and consumer-technology artifacts. `nmah_849914` has limited structured evidence (class B), so retain it only while that scope decision stands.

The remaining reviewed matches have direct evidence for in-scope technologies such as autopilots, radio transmitters and receivers, compasses and gyroscopic instruments, navigation devices, radar, antennas, and typewriters. The manual review supports the v0.2 vocabulary as a useful candidate generator, subject to the false-positive correction and scope decisions above.

### Execution and validation

The selection script reads JSON records from `data/samples/nasm/` and `data/samples/nmah/`, writes a JSON report under `build/`, and must run with the repository root as its working directory. The command-line run from the repository root processed all 200 records. An IntelliJ Run configuration with a different working directory processed zero records; set its working directory to the repository root when using the IDE.

Sixteen focused selection test functions were invoked directly and passed in the implementation environment. The full repository pytest suite was not run there because `pytest` was unavailable.

### Next steps

1. Refine the object-type rule that selected `nasm_A19360009000`, and add the record as a negative regression case.
2. Decide whether V1 includes contextual aircraft/platform records, and review the G-meter domain assignment.
3. Review plausible false negatives from the remaining excluded records and refine field-specific terms only where the source evidence supports them.
4. Run the full repository pytest suite in the project environment.
5. Evaluate a more representative sample and check answerability of Q01–Q15 before selecting the V1 corpus size.

**Deferred:** embeddings, vector database, LLM integration, RAG framework, and production ingestion architecture.

**Resume point:** Step 1.4.3 — correct the identified v0.2 false positive, decide the treatment of contextual aircraft records, and review plausible false negatives before finalizing V1 corpus criteria.
