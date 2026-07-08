---
## ISSUE-001: PDF chunking loses section headers for long policy documents
**Phase**: Phase 3
**Severity**: Warning
**Description**: The chunker splits mid-section on documents over ~40 pages, dropping the header that gives later chunks their context.
**Context**: Found while chunking the 80-page policy PDF from project-context/.
**Impact**: Retrieval on long documents may return chunks without enough context to be useful standalone.
**Suggested resolution**: Carry the nearest preceding header forward into each chunk's metadata.
**Status**: Open
**Date**: 2026-07-06

---
## ISSUE-002: Working directory contains no code — documented Phase 1-3 deliverables are missing
**Phase**: Phase 4 (discovered at session start / resume)
**Severity**: Blocker
**Description**: PROJECT_STATE and PHASE_LOG report Phases 1-3 complete, with specific files created (`pyproject.toml`, `docker-compose.yml`, `.env.example`, `src/ingestion/shopify_loader.py`, `src/ingestion/confluence_loader.py`, `src/ingestion/pdf_loader.py`, `src/embeddings/client.py`, `src/vectorstore/pgvector.py`). None of these files, nor any `src/` tree, exist in the working directory. There is also no git repository (`.git/` is absent, despite the skill's bootstrap step calling for `git init`), no `DEPENDENCY_MANIFEST.md/.json`, no `MODEL_REGISTRY.md/.json`, and the `.project/ADR/` folder is empty despite two decisions logged (BGE-M3 over OpenAI embeddings; PyMuPDF over pdfplumber) that the skill requires an ADR for.
**Context**: Found while re-reading the existing codebase at the start of this session, before trusting the docs' claim that Phase 4 (Retrieval Pipeline) can safely build on a "live" pgvector store and embedding client from Phase 3.
**Impact**: Phase 4 depends concretely on Phase 3's vector store and embedding client. If that code doesn't actually exist, Phase 4 cannot start from the assumed foundation — either the code was lost (workspace reset, uncommitted work, wrong directory) or the prior sessions' logs describe work that was never actually written to disk.
**Suggested resolution**: Ask the user which is true: (a) the code exists elsewhere and this working directory is stale/wrong, (b) the code was lost and needs to be recreated, or (c) treat Phases 1-3 as needing to be redone from the existing docs (which do contain enough decision detail — model choice, library choice, schema intent — to reconstruct quickly). Do not proceed into Phase 4 until this is resolved.
**Status**: Open
**Date**: 2026-07-07
