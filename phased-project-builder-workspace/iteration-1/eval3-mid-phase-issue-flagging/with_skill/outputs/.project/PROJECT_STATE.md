# Project State: Customer Support RAG Agent

**Project Type**: AI/ML - Agentic RAG
**Core Goal**: RAG-based AI agent for Tier-1 customer support with order lookup and escalation
**Created**: 2026-07-05
**Last Updated**: 2026-07-09

---

## Current Status

**Current Phase**: Phase 7 — Tools & Sub-agents
**Status**: In progress — paused mid-phase on ISSUE-001 (Blocker)
**Overall Progress**: 6 of 9 phases complete, Phase 7 partially started
**Last Session**: Session 5 (2026-07-09) — Started Phase 7 with the order-lookup tool. Built `src/tools/order_lookup.py`'s auth-independent parts (validation, response shape, error taxonomy, audit logging). Paused before implementing the HTTP client: `project-context/product-spec.md` and `project-context/addendum-notes-2026-07-08.md` describe two different, mutually exclusive Order Management API contracts (API-key auth vs. OAuth2 client-credentials, different base URLs). Logged as ISSUE-001 and stopped rather than guessing. Escalation tool and orchestrator wiring not started yet.

---

## Phase Plan

1. Scaffold & Environment — complete
2. Data Ingestion — complete
3. Embedding & Vector Store — complete
4. Retrieval Pipeline — complete
5. Intent Classification / Routing — complete
6. Orchestration Layer (LangGraph) — complete
7. Tools & Sub-agents (Order lookup tool, escalation tool) — in progress (depends on 6)
8. Generation & Response Synthesis — not started (depends on 6, 7)
9. Evaluation & Hardening — not started (depends on 8)

## Open Issues

- **ISSUE-001** (Blocker, Phase 7): Order Management API auth/base URL conflict between `project-context/product-spec.md` (API-key auth, `orders.internal.company.com/v1`) and `project-context/addendum-notes-2026-07-08.md` (OAuth2 client-credentials, `orders-v2.internal.company.com`). Blocks finishing the order-lookup tool's HTTP client. See `.project/ISSUES.md`.
