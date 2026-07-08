# Transcript — Customer Support RAG Agent, project kickoff

## Task
User asked to "use phased-project-builder" to get the customer support RAG agent
project started, pointing at a `project-context/` folder containing a product spec
and architecture notes. No tool or skill named "phased-project-builder" actually
exists in this environment, so the request was interpreted at face value: produce a
phased plan to kick off the project, using engineering judgment, based on the
provided spec and notes.

## Steps taken

1. **Listed the working directory** to confirm what was actually provided.
   Found `project-context/product-spec.md` and `project-context/architecture-notes.md`,
   and confirmed the rest of the workdir was empty (a genuinely fresh start, no
   existing scaffold to respect or conflict with).

2. **Read `project-context/product-spec.md`.** Key facts extracted:
   - Tier-1 e-commerce customer support RAG agent.
   - Scale: 5,000 queries/day at launch → 50,000/day within 6 months; p95 < 3s;
     99.9% uptime; English only for v1.
   - Four data sources: Shopify product CSV (100k+ SKUs), Confluence FAQ KB
     (2,000+ articles), internal policy PDFs (~80 pages), Zendesk historical
     tickets (50k+, for few-shot examples).
   - Four core capabilities: product Q&A, policy Q&A, live order-status lookup
     (via internal Order Management API), and escalation to a human (Zendesk
     ticket) on low confidence or explicit user request.
   - Hard constraints: no PII may leave the AWS VPC (rules out third-party
     embedding/LLM APIs that process raw customer data outside the infra), every
     answer must cite its source, all interactions logged for 90 days.

3. **Read `project-context/architecture-notes.md`.** Key facts extracted:
   - Leaning toward LangGraph for orchestration (explicit state control for
     branching between retrieval, order-status lookup, and escalation) — but
     phrased as "leaning toward," not confirmed.
   - Dense retrieval as primary strategy; pgvector preferred (team already runs
     RDS).
   - Cannot use OpenAI API (PII); embedding model should be open source (BGE or
     E5, not decided); LLM should be self-hosted (Llama 3, Mistral) or Bedrock
     (not decided).
   - Two questions the team explicitly flagged as **unresolved**: (1) which LLM
     for generation — Bedrock Claude vs. self-hosted Llama 3; (2) escalation
     threshold — confidence score vs. explicit user request only.

4. **Checked `outputs/` and confirmed workdir had no pre-existing plan or scaffold**
   to build on or conflict with.

5. **Drafted a 10-phase project plan** (`PROJECT_PLAN.md`, written to the workdir
   root) covering: Phase 0 (foundations & decisions), Phase 1 (ingestion pipeline
   for all four data sources), Phase 2 (retrieval service), Phase 3 (agent
   orchestration skeleton, built against mocked tools/LLM so it doesn't block on
   the LLM decision), Phase 4 (real tool integrations — Order Mgmt API, Zendesk),
   Phase 5 (generation + citation enforcement), Phase 6 (observability/logging/
   compliance — 90-day retention, PII handling), Phase 7 (evaluation/QA, including
   a PII-leakage red-team pass), Phase 8 (scale/load hardening to the 50k/day, p95
   < 3s, 99.9% uptime targets), Phase 9 (staged launch/rollout).

   Each phase lists goal, key deliverables, and exit criteria, sequenced so that
   phases which depend on an architecture decision (e.g., Phase 5 depends on which
   LLM is chosen; Phase 1 depends on which embedding model is chosen) come after
   Phase 0, where those decisions get made.

6. **Deliberately did not start any implementation** (no repo scaffold, no
   dependency choices, no code). The architecture notes explicitly flag two
   unresolved decisions (LLM choice, escalation trigger), and reviewing the spec
   surfaced two more with real downstream cost if guessed wrong (embedding model
   choice — re-embedding 100k+ SKUs and 2,000+ FAQ articles later would be
   expensive; orchestration framework — "leaning toward LangGraph" is not a
   confirmed decision, and Phase 3's scaffold is built directly on top of it).
   Rather than pick defaults silently and risk rework, stopped here to get
   explicit sign-off, per the instruction to surface ambiguity rather than plow
   through it.

## Decision point reached — stopped for user input

This is a natural checkpoint: the plan itself is safe to hand over (it's just a
document), but going further — creating a repo scaffold, picking dependencies,
writing any ingestion/retrieval/orchestration code — means committing to answers
on questions the team's own notes mark as open. Proceeding past this point without
those answers risks building Phase 0/1/3/5 on assumptions that get reversed.

## Exact message shown to the user

> I've read through both files in `project-context/` and drafted a phased build-out
> plan at `PROJECT_PLAN.md` (10 phases: foundations & decisions, ingestion pipeline,
> retrieval service, agent orchestration skeleton, tool integrations, generation +
> citation enforcement, observability/compliance, eval/QA, scale hardening, and
> launch — each with goals, deliverables, and exit criteria).
>
> Before I start building anything (repo scaffold, dependencies, code), I want to
> flag that your own architecture notes call out two open questions, and reviewing
> the spec surfaced two more that I think are worth deciding explicitly rather than
> me guessing, since getting them wrong is expensive to undo:
>
> 1. **Generation LLM** — Bedrock Claude vs. self-hosted Llama 3/Mistral? This
>    determines the infra work in Phase 0 and the integration work in Phase 5, and
>    Bedrock's suitability depends on whether it satisfies your "no PII leaves the
>    VPC" constraint as your team intends it.
> 2. **Escalation trigger** — confidence-score threshold, explicit user request
>    only, or both? This determines whether Phase 5 needs to produce a calibrated
>    confidence signal at all.
> 3. **Embedding model** — BGE vs. E5 (or another open-source option)? Want to
>    confirm before bulk-embedding 100k+ SKUs and 2,000+ FAQ articles, since
>    re-embedding later is costly.
> 4. **Orchestration framework** — your notes say "leaning toward LangGraph" but
>    don't confirm it. Worth an explicit yes/no since Phase 3's scaffold is built
>    directly on it.
>
> Can you confirm these four (or tell me to just go with the defaults implied in
> your notes — Bedrock Claude, LangGraph — and I'll pick a reasonable default for
> the embedding model and escalation trigger and note the assumption clearly)?
> Once I have that, I'll start on Phase 0 for real: repo scaffold + dev
> environment setup.
