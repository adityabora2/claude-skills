---
name: codebase-audit
description: Perform a complete, file-by-file audit of a codebase and produce a single comprehensive Markdown report covering architecture, tech stack, use case, data/control flow, and pipeline structure. This skill is invoked explicitly by the user (e.g. "/codebase-audit") and should NOT trigger automatically on generic requests like "explain this repo" or "what does this file do" — only use it when the user explicitly invokes the codebase-audit command/skill by name.
---

# Codebase Audit

Produce a single, complete Markdown audit of a codebase: every file in the repository (respecting `.gitignore`), analyzed at a depth proportional to its size/complexity, tied together with an overall architecture narrative and diagrams.

## When this runs

This skill only runs when the user explicitly invokes it (slash-invoked as `/codebase-audit`, or by literally asking for "a codebase audit" / "run the codebase-audit skill"). Don't proactively suggest or auto-trigger this for ordinary code questions — a full audit is a heavyweight operation, and firing it on an offhand "what does this file do?" would waste a lot of the user's time and tokens for something they didn't ask for.

## Step 1: Establish scope

1. Confirm the root directory to audit (default: current working directory / repo root).
2. Get the full file list, respecting `.gitignore`:
   ```bash
   git ls-files            # if it's a git repo — automatically respects .gitignore
   ```
   If it's not a git repo, there's no `.gitignore` to respect automatically, so build the list manually and exclude the usual noise yourself:
   ```bash
   find . -type f \
     -not -path '*/node_modules/*' -not -path '*/.git/*' \
     -not -path '*/venv/*' -not -path '*/.venv/*' -not -path '*/__pycache__/*' \
     -not -path '*/dist/*' -not -path '*/build/*' -not -path '*/target/*'
   ```
3. Get a rough size read (file count, total lines, language breakdown):
   ```bash
   git ls-files | xargs wc -l | tail -1
   git ls-files | sed 's/.*\.//' | sort | uniq -c | sort -rn   # rough language breakdown by extension
   ```
4. **Scale check.** If this comes back at a few hundred files or more, say so before diving in and confirm the approach: Tier A (deep dive) will focus on the structurally important files, and the report will stay readable rather than becoming a wall of text nobody will read. This is a one-line check-in, not a blocker — default to proceeding with the tiering approach below if the user doesn't have a strong opinion.

## Step 2: Build the file inventory and classify tiers

Create a table of every tracked file: path, language/type, line count, and tier. This becomes the "Appendix: File Inventory" in the final report, and the tier assignment drives how much attention each file gets in Step 4.

**Tier A (deep dive)** — don't rely on gut feel alone; use these signals, and if a file matches any of them, it's Tier A regardless of length:
- **Entry points**: `main.*`, `index.*`, `app.*`, `server.*`, `__main__.py`, `cmd/*`, anything referenced as an entrypoint in a config file (`package.json` "main"/"bin", Dockerfile `CMD`/`ENTRYPOINT`, etc.)
- **High fan-in**: files imported/required by many other files. Approximate this with a quick grep rather than tracing by hand:
  ```bash
  # Python example — count how often each module is imported
  git grep -h -oE '^\s*(from|import)\s+[a-zA-Z_.]+' | awk '{print $2}' | sort | uniq -c | sort -rn | head -20
  ```
  Adjust the pattern for the language in use (`require(`/`import ... from` for JS/TS, etc.)
- **Orchestrators/routers/core logic**: naming patterns like `router`, `orchestrator`, `pipeline`, `service`, `core`, or files defining the main data models/schemas
- **Large or structurally central files**: no fixed line-count threshold, but a good default is "well above the median file size for this repo" (check the line-count column you already have)

**Tier B (summary)** — supporting files, small modules, config, simple components that don't match any Tier A signal.

**Tier C (inventory-only, no prose)** — assets, lockfiles, generated/vendored code, binary files.

## Step 3: Working notes (do this for anything beyond a handful of files)

Reading and writing up hundreds of files in one continuous pass risks losing earlier analysis if the run gets cut short partway through, and makes it hard to track what's left. Instead, process directory-by-directory and persist as you go:

1. Work through the repo one directory/module at a time.
2. After finishing a directory, write its findings to a scratch file (e.g. `/tmp/audit-notes/<module-name>.md`) rather than holding it all in your head for the final assembly step.
3. Give the user a brief progress update as you go (e.g. "Finished `src/api/` — 4 Tier A, 9 Tier B, 2 Tier C"), so a long-running audit stays transparent rather than going quiet for a long stretch.
4. Batch your reads sensibly — use `view` on a whole directory instead of listing files one by one, and `cat` several small Tier B files together in one call rather than one tool call per file. Reserve individual careful reads for Tier A files where you actually need to trace logic.

Once every directory is processed, assemble the final report from these notes rather than re-deriving everything from scratch.

## Step 4: Per-tier analysis depth

- **Tier A — deep dive per file:**
  - Purpose and responsibility
  - Key classes/functions and what each does
  - Inputs/outputs, important data structures
  - Data flow and control flow through the file
  - Dependencies (what it imports/calls, what calls it)
  - Notable patterns, tech/libraries used, and any risks or tech debt actually visible in the code
- **Tier B — one paragraph:** purpose, what it exposes, how it's used elsewhere.
- **Tier C — inventory line only:** no prose analysis, just the table row.

Ground every claim in what you actually read. If you're inferring behavior rather than reading it directly, say so or don't include it — a wrong architectural claim is worse than a missing one.

## Step 5: Synthesize architecture

Step back from the per-file notes and produce the connective narrative:

- **Tech stack**: languages, frameworks, libraries, infra/config actually observed in the files — not assumed from the repo name or README claims alone.
- **Use case**: what the system does end-to-end, inferred primarily from the code (README/docs can supplement but the code is ground truth when they disagree).
- **Architecture**: major components/modules and how they relate (layers, services, packages).
- **Pipeline/data flow**: trace at least one representative end-to-end flow (e.g. a request from entry point to response, or data from ingestion to output) through the actual files, not a generic guess at what such a system "usually" looks like.

## Step 6: Diagrams

Include Mermaid diagrams where they clarify structure — use judgment on which apply, don't force all of them into every audit:
- A component/architecture diagram (`graph TD` or `flowchart`) for major modules and their relationships.
- A sequence or flow diagram for at least one key pipeline/request flow.
- A directory/module structure diagram if the repo's layout itself isn't obvious from the inventory table.

Mermaid is picky about syntax — quote node labels that contain parentheses, colons, or special characters (e.g. `A["parse_config()"]` not `A[parse_config()]`), or the diagram will silently fail to render. Keep each diagram focused on one concern; a diagram trying to show everything ends up showing nothing clearly.

## Step 7: Assemble the report

Produce a single `.md` file with this structure:

```markdown
# Codebase Audit: <repo name>

## 1. Overview
(use case, one-paragraph summary, tech stack table)

## 2. Architecture
(narrative + component diagram)

## 3. Key Pipelines / Data Flow
(narrative + sequence/flow diagram(s) for representative flows)

## 4. Module-by-Module Analysis
(Tier A deep dives, grouped by directory/module)

## 5. Supporting Files Summary
(Tier B one-paragraph summaries, grouped by directory/module)

## 6. Observations & Risks
(tech debt, inconsistencies, missing tests/docs — only what's actually observed, don't manufacture issues to fill the section)

## Appendix: File Inventory
(full table: path | type | lines | tier | one-line purpose)
```

Save the file as `<repo-name>-audit.md` and share it with the user via whatever file-delivery mechanism is available in the current environment (e.g. `present_files`). If none is available, give the file's path directly.

## Notes

- Thoroughness over speed is the point of this skill — for large repos, expect many tool calls and a long response, and that's fine as long as progress is visible (see Step 3).
- Never fabricate function names, file purposes, or architectural claims that aren't backed by what you actually read — an audit the user can't trust is worse than a shorter one they can.