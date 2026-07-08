# Phase Planning Guide

These are starting shapes, not templates to fill in mechanically — always bend them to what the context files actually say. The one rule that doesn't bend: each phase should leave the system in a state that actually runs, not half-wired.

## Table of contents
- [Agentic / RAG systems](#agentic--rag-systems)
- [Multi-agent orchestration systems](#multi-agent-orchestration-systems)
- [Enterprise web applications](#enterprise-web-applications)
- [Data pipelines](#data-pipelines)
- [Sizing a phase](#sizing-a-phase)

## Agentic / RAG systems

Typical for: LLM-powered assistants, document Q&A, research agents, anything that retrieves before it generates.

```
Phase 1: Scaffold & environment
  - Dependency manifest (pyproject.toml / package.json), pinned versions
  - Docker/compose if the context implies containerized deploy
  - .env.example with every required var documented (not just named)
  - Directory structure, structured logging, git init

Phase 2: Data ingestion
  - Loaders for each source named in the context files (CSV, API, PDF, DB export, etc.)
  - Chunking strategy — and a note on *why* that strategy, since it's a common source of
    later rework (e.g. losing section headers in long documents)

Phase 3: Embedding & vector store
  - Embedding model wired up
  - Vector store live and queryable end-to-end on a handful of real records —
    not just "the client connects," but an actual round-trip retrieval

Phase 4: Retrieval pipeline
  - Query embedding, similarity search, ranked-chunk return with source metadata
  - This is the first phase worth writing an eval for: retrieval precision/recall
    on a small hand-picked query set, so later phases don't silently regress it

Phase 5: Intent classification / routing (if the context calls for it)
  - Decide what routes to retrieval vs. a tool call vs. escalation, and on what signal

Phase 6: Orchestration layer
  - The actual agent graph/state machine (LangGraph or equivalent) wiring the above
    stages together — this phase depends on 2-5 already working in isolation,
    since debugging retrieval *and* orchestration *and* routing at once is painful

Phase 7: Tools & sub-agents
  - Each tool/sub-agent defined with a narrow, testable contract
  - Wire into the orchestrator one at a time, not all at once

Phase 8: Generation & response synthesis
  - Prompting for the final answer, citation of sources, guardrails on hallucination

Phase 9: Evaluation & hardening
  - End-to-end eval set, latency/cost check against any stated targets,
    escalation-path testing
```

Skip phases that don't apply (no routing needed? drop Phase 5) and split ones that are doing too much (Phase 7 across 6 tools that don't interact might be 6 phases, one per tool, if each is substantial).

## Multi-agent orchestration systems

Typical for: systems with several specialized agents coordinated by an orchestrator (e.g. a document-parsing agent, a classification agent, a synthesis agent).

```
Phase 1: Scaffold & environment
  - Dependency manifest, pinned versions, Docker/compose if implied
  - .env.example, directory structure, structured logging, git init

Phase 2: Shared state schema
  - Decide once, up front, exactly what the orchestrator passes between agents
    (and what each agent is allowed to read/write) — retrofitting the state shape
    after agents already exist is expensive, since every agent's contract depends on it

Phase 3: Orchestrator skeleton
  - Routes to stub agents that just echo their input back
  - Lets the control flow (routing, error paths, aggregation) be verified before any
    agent has real logic, so a bug is obviously "orchestration" or obviously "an agent,"
    never both at once

Phase 4+: One phase per agent
  - Each phase replaces one stub with real logic and its own narrow tests
  - Build and verify each agent in isolation before wiring the next, so a regression
    always traces back to the one agent that just changed

Phase N: Cross-agent integration
  - Parallel vs. sequential execution between agents, error propagation across agent
    boundaries, aggregation of their outputs into a single result

Phase N+1: Multi-tenancy / isolation, audit trail, evaluation (if the context calls for it)
  - Per-tenant data isolation and audit logging are much harder to retrofit than to
    build in from this phase onward, if the project has any multi-tenant requirement
```

The key idea distinguishing this from a single-agent build: get the *shape* of the orchestrator right early with stub agents, because the coordination logic is usually harder to retrofit than any individual agent's internals.

## Enterprise web applications

Typical for: internal tools, customer-facing web apps, CRUD-heavy business systems, anything organized around a data model and user-facing flows.

```
Phase 1: Scaffold, environment, CI skeleton
  - Auth strategy decided (even if not fully implemented yet) — retrofitting auth
    into domain logic and routes written without it in mind is a common source of rework

Phase 2: Data model & schema
  - Migrations set up from the start, not bolted on later, since schema change
    management only gets harder the more code depends on the shape being fixed

Phase 3: Core domain logic
  - The part with actual business rules, tested in isolation from any API or UI —
    this is what should be hardest to get wrong and easiest to unit-test, so it
    shouldn't be entangled with HTTP or rendering concerns

Phase 4: API layer over the domain logic
  - Thin by design: the API translates requests/responses, it shouldn't contain
    business rules that belong in Phase 3

Phase 5: UI, one major flow at a time
  - Not "all pages" as a single phase — each flow (e.g. sign-up, checkout, admin
    dashboard) is its own phase so a broken flow doesn't block an unrelated one
    from shipping

Phase 6: Cross-cutting concerns
  - Auth enforcement, rate limiting, observability — these touch every phase above,
    so they're deliberately sequenced after the flows exist to enforce them against,
    rather than guessed at in the abstract

Phase 7: Hardening
  - Load/security considerations the context flagged, deployment config, anything
    that only matters once the system is close to handling real traffic
```

## Data pipelines

Typical for: ETL/ELT jobs, scheduled batch processing, anything that moves and reshapes data between systems.

```
Phase 1: Scaffold & environment
  - Dependency manifest, pinned versions, config/secrets handling, git init

Phase 2: Extraction
  - A loader per source, each independently testable against a small real sample —
    so a broken source is isolated immediately instead of surfacing as a mysterious
    downstream data-quality issue

Phase 3: Transformation logic
  - The messy edge cases the context files mention (partial records, schema drift,
    dedup rules) handled explicitly, with a named rule for each rather than silently
    dropping or guessing on bad rows

Phase 4: Load / sink
  - Built with idempotency considered from the start: can this phase's output be
    safely re-run without double-writing? Retrofitting idempotency after a pipeline
    is already writing to a shared destination is far riskier than designing for it here

Phase 5: Orchestration & scheduling
  - Wires extraction → transform → load into one schedulable unit, once each stage
    already works standalone

Phase 6: Monitoring, alerting, backfill strategy
  - How failures are noticed and how a bad run gets safely replayed — easy to skip,
    expensive to be missing the first time a job silently fails for a week
```

## Sizing a phase

Two failure modes to watch for when drafting the plan:

- **Too big**: if a phase's deliverables list reads like three unrelated things bolted together ("build the retriever, wire the orchestrator, AND add the UI"), that's a sign it should split. A phase that can't plausibly finish in one sitting defeats the entire point of phasing.
- **Too small**: a phase that's just "install a package" or "write one config file" with no other content usually belongs folded into the phase that actually uses it — otherwise the plan balloons into noise and the approval step becomes tedious rather than useful.

A good gut check: could you write a one-sentence "what exists now that didn't before" for this phase that a non-technical stakeholder would find meaningful? If not, it's probably mis-sized.
