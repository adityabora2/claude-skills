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
