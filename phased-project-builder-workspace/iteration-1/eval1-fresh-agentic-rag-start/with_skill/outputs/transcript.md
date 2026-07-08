# Transcript — phased-project-builder eval (fresh start, agentic RAG)

## Step-by-step narration

1. **Read the skill file** at `phased-project-builder/SKILL.md` in full to establish the operating procedure.
2. **Read the reference files** named by the skill:
   - `phased-project-builder/references/phase-planning-guide.md` — used the "Agentic / RAG systems" worked example as the base shape for the phase plan.
   - `phased-project-builder/references/documentation-schema.md` — noted the JSON schema for `.project/` docs, to be used once bootstrapping actually happens (not reached this session).
3. **Checked working directory state** (`ls` on the workdir): found no `.project/` directory, but `project-context/` present with two files (`architecture-notes.md`, `product-spec.md`). Per the skill's "Session start" decision tree, this is **Fresh Mode** (rule 2: no `.project/`, but `project-context/` has files).
4. **Read every file in `project-context/`** in full (not sampled), per "Starting a new project" step 1:
   - `product-spec.md` — overview, scale/latency/availability targets, data sources, core capabilities, hard constraints (no PII leaves AWS VPC, mandatory citations, 90-day audit logging).
   - `architecture-notes.md` — preliminary architecture leanings (LangGraph, pgvector, open-source embeddings, Bedrock/self-hosted LLM), plus two explicitly-flagged open questions (LLM choice, escalation threshold).
5. **Extracted**: core goal, requirements, tech stack signals, architecture hints, and gaps, as instructed.
6. **Produced the Context Summary** per the required template, classifying the two explicitly-unresolved architecture questions as Blockers (they don't change the phase *shape*, but they gate specific phase decisions — Phase 8 for LLM choice, Phase 5 for escalation trigger) and the remaining defaults (embedding model, vector store, deploy tooling, credential handling) as Assumptions to proceed with unless corrected.
7. **Proposed a 9-phase plan**, adapted from the phase-planning-guide's "Agentic / RAG systems" template but tailored to the spec's specifics (e.g., explicit ingestion loaders per named source, audit-logging called out early in Phase 1, Order Management API + Zendesk ticket tools named explicitly in Phase 7, p95 latency and 90-day audit verification named explicitly in Phase 9).
8. **Stopped per the skill's instruction**: "Then pause and wait for explicit approval. Don't start writing code after just showing the plan." No `.project/` scaffold was created, no application code was written, and no git repo was initialized, since approval was not yet given (this is a scripted eval with no human available to respond — the correct behavior is to stop here).

## Final message shown to the user (verbatim)

Confirmed Fresh Mode: no `.project/` exists, `project-context/` has the two spec files. Now producing the Context Summary and phase plan per the skill, then stopping for approval as instructed.

---

## Context Summary
**Project Name**: Customer Support RAG Agent
**Project Type**: AI/ML — Agentic RAG (LangGraph orchestration, tool-calling, escalation)
**Core Goal**: A RAG-based AI agent that answers Tier-1 e-commerce customer support questions (orders, returns, shipping, product info) by retrieving from a knowledge base, looking up live order status, and escalating to a human when needed.

**Key Requirements**:
- Traffic: 5,000 queries/day at launch → 50,000/day within 6 months
- Latency: p95 < 3s; Availability: 99.9%
- English only for v1
- Data sources: Shopify product catalog (CSV, 100k+ SKUs), Confluence FAQ KB (2,000+ articles), internal policy PDFs (~80 pages), Zendesk historical tickets (50k+, for few-shot)
- Core capabilities: product Q&A, policy Q&A, live order-status lookup via internal Order Management API, escalation to human (creates Zendesk ticket) on low confidence or explicit request
- Every AI answer must cite its source
- All interactions logged for 90 days (audit)

**Tech Stack Signals**:
- Orchestration: LangGraph (explicit state control for branching between retrieval / order-status tool / escalation)
- Retrieval: dense embeddings, pgvector (team already runs RDS)
- Embedding model: open-source preferred (BGE, E5 mentioned)
- Generation LLM: self-hosted (Llama 3, Mistral) or Amazon Bedrock — both keep data in-VPC
- Cloud: AWS (RDS, VPC, Bedrock); integrations with Zendesk, Confluence, Shopify, internal Order Management API

**Open Questions**:
- **[Blocker]** Which LLM backs generation — Bedrock Claude vs. self-hosted Llama 3/Mistral? The architecture notes flag this as explicitly unresolved. It doesn't change the phase *shape* below, but it does gate implementation decisions in Phase 8 (and infra/dependency choices in Phase 1) — I'll need an answer before those phases execute.
- **[Blocker]** Escalation trigger — automatic on a confidence score, or only on explicit user request for a human? This shapes the routing logic built in Phase 5. Also flagged as unresolved in the architecture notes.
- **[Assumption]** Embedding model: will default to an open-source model (e.g., BGE-M3) given the PII/self-hosted constraint, unless corrected.
- **[Assumption]** Vector store: pgvector on the existing RDS instance, as stated — no alternative needed.
- **[Assumption]** Confluence/Zendesk/Shopify/Order Management API credentials will be supplied via `.env` when we reach the phases that need them; not blocking scaffolding.
- **[Assumption]** No containerized deploy target was specified explicitly — I'll assume Docker/compose for local dev parity with the AWS/VPC target unless told otherwise.

---

## Proposed Phase Plan

### Phase 1: Scaffold & Environment
**Goal**: A running project skeleton with dependencies, config, structured logging, and directory layout in place.
**Deliverables**: `pyproject.toml` (pinned: LangGraph, pgvector client, embedding lib, boto3), `.env.example` documenting every required var (AWS/RDS, Bedrock or self-hosted LLM endpoint, Confluence/Zendesk/Shopify/Order Mgmt API creds), directory structure (`src/ingestion`, `src/embeddings`, `src/vectorstore`, `src/retrieval`, `src/routing`, `src/orchestration`, `src/tools`, `src/generation`, `eval/`), structured logging wired up (needed early given the 90-day audit-logging requirement), git init.
**Depends on**: None

### Phase 2: Data Ingestion
**Goal**: Every data source named in the spec can be loaded into a common document schema.
**Deliverables**: Loaders for Shopify CSV catalog, Confluence FAQ export, policy PDFs, Zendesk historical tickets; a documented chunking strategy per source type (with explicit reasoning — e.g. header-carry-forward for long PDFs); common document schema carrying source metadata for later citation.
**Depends on**: Phase 1

### Phase 3: Embedding & Vector Store
**Goal**: An open-source embedding model and pgvector store are live and verified end-to-end.
**Deliverables**: Embedding client (default: BGE-M3, pending confirmation), pgvector schema + upsert/query code, verified round-trip retrieval on a handful of real sample records from each source.
**Depends on**: Phase 2

### Phase 4: Retrieval Pipeline
**Goal**: Given a query, the system returns ranked, source-attributed chunks.
**Deliverables**: Query embedding + similarity search + ranked-chunk return with source metadata; a small hand-picked eval set covering product/policy/FAQ queries with precision/recall measured, so later phases don't silently regress retrieval quality.
**Depends on**: Phase 3

### Phase 5: Intent Classification & Routing
**Goal**: Incoming queries are routed to the right path — retrieval, order-status tool, or escalation.
**Deliverables**: Router that classifies product/policy questions → retrieval, order-status questions → Order Management API tool, explicit human requests (or low-confidence cases, pending the escalation-threshold answer) → escalation.
**Depends on**: Phase 4 (blocked in part on the escalation-trigger answer above)

### Phase 6: Orchestration Layer (LangGraph)
**Goal**: A working LangGraph state machine wires routing, retrieval, and escalation into one coherent agent flow.
**Deliverables**: LangGraph graph/state definition connecting Phases 2–5 as isolated, already-working stages.
**Depends on**: Phase 5

### Phase 7: Tools & Integrations
**Goal**: External-system actions the agent can take are implemented and wired in one at a time.
**Deliverables**: Order Management API tool (live order-status lookup), Zendesk ticket-creation tool (escalation handoff), each with a narrow, testable contract.
**Depends on**: Phase 6

### Phase 8: Generation & Response Synthesis
**Goal**: The agent produces final answers with mandatory source citation and hallucination guardrails.
**Deliverables**: Generation prompt(s) against the chosen LLM, citation formatting, confidence signal feeding the escalation path.
**Depends on**: Phase 7 (blocked on the LLM-choice answer above)

### Phase 9: Evaluation & Hardening
**Goal**: The system is measured end-to-end against the spec's stated targets and hardened for launch.
**Deliverables**: End-to-end eval set across all four capabilities, latency check against the p95 < 3s target at expected load, audit-logging verification (90-day retention), escalation-path testing.
**Depends on**: Phase 8

---

Here's the proposed phase breakdown — let me know if you want to change anything (reorder, merge, split), and let me know your answers on the two blockers above (LLM choice, escalation trigger), or say "approved" to start Phase 1 with the stated assumptions.

## Stopping point

This is the correct, complete end state for this session: the skill instructs to "pause and wait for explicit approval" after presenting the phase plan, and not to start writing code or bootstrapping `.project/` until that approval is given. No `.project/` directory, git repo, or application code was created. No files exist yet beyond the pre-existing `project-context/` inputs.
