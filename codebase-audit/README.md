# Codebase Audit Skill

A Claude skill that produces a complete, file-by-file audit of a codebase as a single Markdown report — architecture, tech stack, use case, data/control flow, and pipeline structure, all grounded in what's actually in the repo.

## What it does

Given a repository, this skill:

1. Lists every tracked file (respecting `.gitignore`)
2. Classifies each file into a tier based on concrete signals (entry points, import fan-in, naming patterns, relative size) rather than vague judgment calls
3. Analyzes files at a depth matched to their tier:
   - **Tier A** (core/complex files) — full deep dive: purpose, key functions/classes, data flow, dependencies, notable risks
   - **Tier B** (supporting files) — one-paragraph summary
   - **Tier C** (assets, lockfiles, generated code) — inventory line only, no prose
4. Synthesizes an overall architecture narrative: tech stack, use case, component relationships, and at least one traced end-to-end pipeline/data flow
5. Adds Mermaid diagrams where they clarify structure (component diagram, key flow diagram, directory structure if non-obvious)
6. Assembles everything into a single `<repo-name>-audit.md` report with a fixed section structure (Overview → Architecture → Key Pipelines → Module-by-Module Analysis → Supporting Files Summary → Observations & Risks → File Inventory appendix)

For large repositories (a few hundred files or more), it works directory-by-directory, persists notes to a scratch file as it goes, and gives progress updates — so a long audit is resumable and transparent rather than a single opaque pass that loses everything if interrupted.

## When it triggers

**Only on explicit invocation** — e.g. `/codebase-audit`, or literally asking to "run a codebase audit" / "run the codebase-audit skill". It's deliberately written to *not* fire on generic requests like "explain this repo" or "what does this file do", since a full audit is a heavyweight operation that shouldn't run unprompted.

## Output

A single Markdown file: `<repo-name>-audit.md`, containing the full report described above plus a complete file inventory table as an appendix.

## Notes

- Works best run from the repository root.
- Every claim in the report is meant to be grounded in files actually read — it's written to flag uncertainty rather than fabricate architectural claims or function behavior it hasn't verified.
- Not built for non-git repositories' `.gitignore` handling — if there's no git repo, it falls back to a manual exclusion list for common noise directories (`node_modules`, `venv`, `dist`, etc.) instead of true `.gitignore` parsing.