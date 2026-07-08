# Project State: Customer Support RAG Agent

**Project Type**: AI/ML - Agentic RAG
**Core Goal**: RAG-based AI agent for Tier-1 customer support with order lookup and escalation
**Created**: 2026-07-05
**Last Updated**: 2026-07-06

---

## Current Status

**Current Phase**: Phase 4 — Retrieval Pipeline
**Status**: Not yet started
**Overall Progress**: 3 of 9 phases complete
**Last Session**: Session 2 (2026-07-06) — Completed Phase 3 (Embedding & Vector Store). Vector store is live with pgvector on RDS, BGE-M3 embeddings indexing working. One open issue on chunking strategy for policy PDFs.

---

## Phase Plan

1. Scaffold & Environment — complete
2. Data Ingestion — complete
3. Embedding & Vector Store — complete
4. Retrieval Pipeline — not started (depends on 3)
5. Intent Classification / Routing — not started (depends on 4)
6. Orchestration Layer (LangGraph) — not started (depends on 4, 5)
7. Tools & Sub-agents (Order lookup, escalation) — not started (depends on 6)
8. Generation & Response Synthesis — not started (depends on 6, 7)
9. Evaluation & Hardening — not started (depends on 8)

---

## Session History

- Session 1 (2026-07-05): Bootstrapped docs, completed Phase 1 (scaffold) and Phase 2 (data ingestion loaders for CSV/Confluence/PDF).
- Session 2 (2026-07-06): Completed Phase 3 — BGE-M3 embeddings + pgvector on RDS, verified round-trip retrieval on sample docs. Flagged ISSUE-001 on PDF chunking.

## Open Issues

- ISSUE-001 (Warning): PDF chunking loses section headers for long policy documents.
