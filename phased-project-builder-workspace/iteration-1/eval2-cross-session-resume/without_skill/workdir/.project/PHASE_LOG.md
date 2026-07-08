---
## Phase 1: Scaffold & Environment — 2026-07-05
**Status**: Complete
**Summary**: Set up pyproject.toml, Docker/compose, .env.example, structured logging, git init.
**Files created/modified**:
- `pyproject.toml` — pinned deps
- `docker-compose.yml` — local Postgres + app container
- `.env.example` — all required vars documented
**Key decisions**: None significant.
**Issues flagged**: None
**Dependencies added**: fastapi, langgraph, boto3

---
## Phase 2: Data Ingestion — 2026-07-05
**Status**: Complete
**Summary**: Built loaders for Shopify CSV export, Confluence FAQ API, and internal policy PDFs.
**Files created/modified**:
- `src/ingestion/shopify_loader.py`
- `src/ingestion/confluence_loader.py`
- `src/ingestion/pdf_loader.py`
**Key decisions**: Chose PyMuPDF over pdfplumber for PDF loader — faster on the 80-page policy doc in testing.
**Issues flagged**: None
**Dependencies added**: pymupdf, atlassian-python-api

---
## Phase 3: Embedding & Vector Store — 2026-07-06
**Status**: Complete
**Summary**: BGE-M3 embeddings wired up, pgvector live on RDS, verified round-trip retrieval on 20 sample docs.
**Files created/modified**:
- `src/embeddings/client.py` — BGE-M3 embedding client
- `src/vectorstore/pgvector.py` — connection + upsert/query
**Key decisions**: Chose BGE-M3 over OpenAI embeddings — context rules out external API calls for PII reasons; BGE-M3 is open-source and self-hostable.
**Issues flagged**: ISSUE-001
**Dependencies added**: pgvector==0.2.4
**AI/ML components**: Added Document Embedder entry to MODEL_REGISTRY (BGE-M3)
