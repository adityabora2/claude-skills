# Project State: Customer Support RAG Agent

**Project Type**: AI/ML - Agentic RAG
**Core Goal**: RAG-based AI agent for Tier-1 customer support with order lookup and escalation
**Created**: 2026-07-05
**Last Updated**: 2026-07-09

---

## Current Status

**Current Phase**: Phase 7 — Tools & Sub-agents
**Status**: Blocked — clarification needed before order-lookup tool can be built (see ISSUE-1)
**Overall Progress**: 6 of 9 phases complete
**Last Session**: Session 5 (2026-07-07) — Started Phase 7 (order-lookup tool). Found that `project-context/product-spec.md` and `project-context/addendum-notes-2026-07-08.md` describe conflicting Order Management API integrations (different base URL and auth mechanism). Flagged as ISSUE-1 and stopped before writing tool code, pending user clarification.

---

## Phase Plan

1. Scaffold & Environment — complete
2. Data Ingestion — complete
3. Embedding & Vector Store — complete
4. Retrieval Pipeline — complete
5. Intent Classification / Routing — complete
6. Orchestration Layer (LangGraph) — complete
7. Tools & Sub-agents (Order lookup tool, escalation tool) — not started (depends on 6)
8. Generation & Response Synthesis — not started (depends on 6, 7)
9. Evaluation & Hardening — not started (depends on 8)

## Open Issues

- **ISSUE-1** (blocking, Phase 7): Order Management API integration details conflict between `product-spec.md` (API-key auth, `orders.internal.company.com/v1`) and `addendum-notes-2026-07-08.md` (OAuth2 client-credentials, `orders-v2.internal.company.com`). See `.project/ISSUES.md`. Awaiting user clarification.
