# Customer Support RAG Agent — Phased Project Plan (Draft v0.1)

Source documents: `project-context/product-spec.md`, `project-context/architecture-notes.md`

This is a first-pass phase breakdown to get the project moving. It is intentionally
sequenced so that unresolved architecture decisions get made (Phase 0) before any
code that depends on them gets written. **Three open items block a confident Phase 0
sign-off — see "Blocking decisions" at the bottom before this plan is treated as final.**

---

## Phase 0 — Foundations & Decisions
Goal: lock the architecture choices the spec/notes leave open, and stand up the repo
skeleton, so later phases aren't built on assumptions that get reversed later.

- Resolve the 4 blocking decisions listed at the end of this doc.
- Define repo structure (ingestion / retrieval / agent / api / eval directories).
- Stand up dev environment: AWS VPC access, RDS+pgvector instance (dev tier),
  credentials/secrets handling for Shopify, Confluence, Zendesk, Order Mgmt API.
- Write the data-handling / PII policy as an explicit doc (what never leaves the VPC,
  how logs are scrubbed) — this gates Phase 1 ingestion design.
- Exit criteria: architecture decision doc signed off; empty repo scaffold with CI
  stub deployed; dev VPC resources provisioned.

## Phase 1 — Knowledge Ingestion Pipeline
Goal: get all four data sources into a chunked, embedded, queryable state.

- Connectors: Shopify CSV (product catalog, 100k+ SKUs), Confluence FAQ export
  (2,000+ articles), policy PDFs (~80 pages), Zendesk historical tickets (50k+,
  for few-shot examples only, not for live retrieval unless decided otherwise).
- Chunking strategy per source type (product rows vs. prose FAQ vs. PDF policy text).
- Embedding generation using the chosen open-source model (see blocking decision #3).
- Load into pgvector with metadata needed for citations (source doc, section, URL/ID).
- Exit criteria: all four sources ingested end-to-end in a dev pgvector instance;
  spot-check retrieval returns sane neighbors for ~20 hand-picked queries.

## Phase 2 — Core Retrieval Service
Goal: a standalone retrieval API the agent can call.

- Dense retrieval query path against pgvector; basic relevance filtering/reranking.
- Citation metadata surfaced alongside every retrieved chunk (spec requires every
  answer to cite its source).
- Exit criteria: retrieval service returns top-k chunks + citations for a query in
  isolation, with latency budget carved out of the overall p95 < 3s target.

## Phase 3 — Agent Orchestration Skeleton
Goal: the branching control flow described in the architecture notes (retrieval vs.
order lookup vs. escalation), independent of which LLM ends up plugged in.

- State graph with explicit branches: answer-from-KB, order-status-lookup, escalate.
- Stub/mock the LLM call and the Order Management API call at this stage so the
  control flow can be tested before Phase 0's LLM decision is fully wired up.
- Exit criteria: orchestration graph runs end-to-end on mocked tools/LLM for a set
  of scripted scenarios covering all three branches.

## Phase 4 — Tool Integrations
Goal: replace stubs with real integrations.

- Order Management API client (live order status lookups).
- Zendesk ticket creation on escalation.
- Error handling / retries / timeouts for both (these sit on the latency-critical
  path for p95 < 3s).
- Exit criteria: real order lookups and real ticket creation work against
  staging/sandbox endpoints.

## Phase 5 — Generation & Citation Enforcement
Goal: wire in the actual LLM and enforce the "always cite sources" constraint.

- Prompt templates that force citation of retrieved chunk IDs.
- Post-generation check: reject/flag answers that don't cite anything.
- Confidence signal for use in the escalation branch (pending blocking decision #2).
- Exit criteria: generated answers reliably include verifiable citations across the
  Phase 1 test query set; confidence signal available to the orchestration layer.

## Phase 6 — Observability, Logging & Compliance
Goal: meet the audit and PII constraints, not just the functional ones.

- 90-day interaction logging (spec requirement) with PII handling consistent with
  the Phase 0 data-handling policy.
- Metrics/tracing for latency (p95), error rates, escalation rate.
- Exit criteria: dashboard showing p95 latency, uptime proxy, escalation rate;
  log retention verified against the 90-day requirement.

## Phase 7 — Evaluation & QA
Goal: confidence that the system is actually good, not just functional.

- Golden test set covering product questions, policy questions, order lookups,
  and forced-escalation cases.
- Accuracy/groundedness evaluation (citations actually support the claim made).
- PII-leakage red-team pass given the hard VPC constraint.
- Exit criteria: eval suite passing at an agreed threshold; no PII-leakage findings.

## Phase 8 — Scale & Load Hardening
Goal: go from "works" to "works at 5k/day → 50k/day within the latency/availability SLA."

- Load testing at both traffic tiers.
- Caching (e.g., embedding cache, frequent-FAQ cache) and autoscaling for retrieval
  and generation services.
- Exit criteria: p95 < 3s and simulated 99.9% availability demonstrated at 50k/day
  load in a staging environment.

## Phase 9 — Launch & Rollout
Goal: controlled production rollout.

- Staged rollout (shadow mode → limited % → full traffic).
- On-call runbook, rollback plan, escalation-path fallback if the agent is down.
- Exit criteria: full production traffic served within SLA for an agreed burn-in
  period.

---

## Blocking decisions (need your input before Phase 0 can be considered done)

These are called out explicitly as unresolved in `architecture-notes.md`, plus two
more that fall out of them. Each has real downstream cost, so I'd rather confirm
than assume:

1. **Generation LLM**: Bedrock Claude (in-VPC via AWS, less ops burden, but need to
   confirm Bedrock's data-handling satisfies the "no PII leaves our VPC" constraint
   as written) vs. self-hosted Llama 3 / Mistral (more control, more infra/ops work —
   GPU provisioning, model serving, scaling). This changes Phase 0's infra
   provisioning and Phase 5's integration work substantially.
2. **Escalation trigger**: confidence-score threshold vs. explicit-user-request-only
   vs. a hybrid. This changes what Phase 5 needs to produce (a calibrated confidence
   signal or not) and what Phase 3's escalation branch checks.
3. **Embedding model**: BGE vs. E5 (or another open-source option). Affects Phase 1
   ingestion and Phase 2 retrieval quality/tuning; want to confirm before bulk-
   embedding 100k+ SKUs and 2,000+ FAQ articles, since re-embedding later is costly.
4. **Orchestration framework**: notes say "leaning toward LangGraph" but don't
   confirm it. Worth a quick explicit sign-off since Phase 3's scaffold is built
   directly on top of whatever we pick.

I have not started any implementation (no repo scaffold, no dependencies chosen)
pending answers to these — they'd otherwise need to be redone if the answers differ
from my defaults.
