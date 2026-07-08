---
name: phased-project-builder
description: Builds an enterprise or production-grade project (especially AI/ML systems — agentic frameworks, RAG pipelines, LangGraph orchestrators) from scratch, using only the requirement/spec files the user drops in a project-context/ folder. Executes the build as a sequence of small, approved phases instead of one long run, because a single continuous build reliably runs out of context or usage budget partway through and leaves the project in an unknown state. Maintains a persistent .project/ documentation trail (state, phase history, issues, decisions, and — for AI/ML work — a model/prompt registry) so that a brand-new chat session, days or weeks later, can pick up exactly where the last one left off without the user re-explaining anything. Only invoke this skill when the user explicitly names it (e.g. "use phased-project-builder", "@phased-project-builder") — do not trigger it automatically just because a project-context/ folder or a build request is present.
---

# Phased Project Builder

## The problem this solves

Building a real system in one shot doesn't work well when the builder (you) has a hard context/usage ceiling. If a build runs long enough, it stops mid-thought, and whoever picks it up next — a new session, or the same session after a summary — has no reliable way to know what was actually finished, what was half-done, and why earlier choices were made. The fix isn't "try to fit it in one go," it's to make each unit of work small enough to finish and document well enough that stopping is never destructive.

So this skill has two equally important halves: **building in phases**, and **writing down enough that memory loss is recoverable**. Treat the documentation half as seriously as the code — for this skill, a phase that isn't logged is a phase that didn't happen, because the next session has no other way to know about it.

## Session start: figure out which mode you're in

Before anything else, check the working directory:

1. **`.project/PROJECT_STATE.md` exists** → **Resume Mode**. Read it in full — do not skim. Also skim `.project/ISSUES.md` for anything open. Then go to "Resuming a project" below. Do not ask the user what they want first; orient them, because they may be starting a session with zero memory of their own of what happened last time.
2. **No `.project/`, but `project-context/` has files** → **Fresh Mode**. Go to "Starting a new project" below.
3. **Neither exists** → Ask the user to put their requirement/spec files (specs, notes, architecture docs, data samples — anything describing the intended system) into a `project-context/` folder, then stop and wait.

## Starting a new project

### 1. Read everything in project-context/

Read every file there — don't sample. These are usually `.md` or plain text: specs, notes, architecture thinking, open questions the user already flagged themselves. Extract:

- The core goal, in one sentence
- Concrete requirements (functional and non-functional — scale, latency, compliance, data residency, whatever's stated)
- Tech stack signals — named or implied (languages, frameworks, model providers, vector stores, orchestration tools)
- Architecture hints the user already has opinions about
- Gaps: things left ambiguous or simply not addressed

Then produce a Context Summary for the user before doing anything else:

```
## Context Summary
**Project Name**: ...
**Project Type**: ...
**Core Goal**: [one sentence]
**Key Requirements**: ...
**Tech Stack Signals**: ...
**Open Questions**:
- [Blocker]: can't plan around this without an answer
- [Assumption]: will proceed with this default unless corrected
```

Blockers get asked about directly and you wait for the answer. Assumptions get stated and you move on — don't manufacture a question just to have one.

### 2. Propose the phase plan — then stop

Break the build into phases. There's no fixed template — the right shape depends entirely on what's being built (see `references/phase-planning-guide.md` for worked examples across a few common project shapes, including an agentic/RAG one). What matters is the reasoning behind the split, not matching an example verbatim:

- Each phase should leave the project in a coherent, working state — not a half-wired feature.
- Each phase should be small enough to plausibly finish inside one session. If a phase feels like it's really two phases wearing a trenchcoat, split it.
- Later phases should depend on concrete outputs of earlier ones (a schema, an interface, a working pipeline stage), not vague ordering like "backend then frontend."

Format each phase like this:

```
### Phase N: [Name]
**Goal**: what exists after this phase that didn't before
**Deliverables**: specific files/modules/configs that will exist
**Depends on**: Phase N-1, or None
```

**Then pause and wait for explicit approval.** Don't start writing code after just showing the plan — the user needs a real chance to reorder, merge, split, or reject phases before anything is built, since re-planning after code exists is much more expensive than re-planning before. Say something like: "Here's the proposed phase breakdown — let me know if you want to change anything, or say 'approved' to start Phase 1."

### 3. Bootstrap `.project/` before any application code

Once approved, create the documentation scaffold first. This ordering matters: the docs are what make the project resumable, so they need to exist even if the session ends one line into Phase 1.

```
.project/
├── PROJECT_STATE.md / .json      # current phase, session history, open issues — the front door
├── PHASE_LOG.md / .json          # append-only record of every completed phase
├── ISSUES.md / .json             # everything flagged, open and resolved
├── DEPENDENCY_MANIFEST.md / .json
├── MODEL_REGISTRY.md / .json     # AI/ML projects only — see below
└── ADR/ADR-000-initial-architecture.md
```

Every doc gets **both** a `.md` and a `.json` form with the same information: the Markdown is for a human (or a Claude) to read and understand narratively, the JSON is so a future session can parse phase history programmatically instead of re-reading prose to answer "did we already decide on X." See `references/documentation-schema.md` for the exact JSON shape of each file.

Initialize `PROJECT_STATE.md`/`.json` with the full phase plan, current phase = 1, session count = 1. Init git and commit the scaffold:

```bash
git init
git add .project/
git commit -m "chore: bootstrap project docs and phase plan"
```

Then start Phase 1.

## Resuming a project

Read `.project/PROJECT_STATE.md` and `.json` fully, plus open items in `ISSUES.md`. Then give the user a brief before asking anything:

```
## Resuming: [Project Name]
**Session**: #N
**Last completed**: Phase N — [Name] ([date])
**Next up**: Phase N+1 — [Name]
**Open issues**: [count] — [titles, or "None"]
**Overall progress**: N of M phases complete

[One sentence on where things actually stand.]
```

Then ask: "Ready to continue with Phase N+1, or want to look at the open issues first?" Wait for confirmation before writing code — the user may want to redirect based on what they see, and code written before that redirect is wasted work.

## Running a phase

Before starting: re-read that phase's deliverables from the plan, check for open issues that touch this phase, and actually read the existing relevant code rather than assuming what's there from the docs alone — the docs describe intent, the code is ground truth.

State your approach in a few bullets before writing code, so the user can redirect early if your read on the phase is off.

Build incrementally rather than all-at-once, and narrate meaningfully as you go — not a play-by-play of every line, but enough that someone skimming later knows what happened and why.

### When something's wrong: flag it, don't silently route around it

This skill's self-healing is **flag-only** — surface the problem and stop, rather than quietly patching around it. The reasoning: an autonomous fix that turns out to be wrong is much more expensive to unwind later (across sessions, potentially by a different Claude with no memory of making the fix) than a short pause now to ask the user. If you hit something broken, ambiguous, or that conflicts with an earlier decision:

1. Stop the current thread of work.
2. Append an entry to `.project/ISSUES.md` / `.json`:

```
## ISSUE-N: [short title]
**Phase**: Phase N
**Severity**: Blocker | Warning | Note
**Description**: what's wrong, specifically
**Context**: what you were doing when this came up
**Impact**: what can't proceed until this is resolved
**Suggested resolution**: your best read on what to do
**Status**: Open
**Date**: YYYY-MM-DD
```

3. Report it to the user and ask how to proceed. A Blocker means stop and wait; a Warning or Note can sometimes be logged and worked around for now, but say so explicitly rather than deciding silently.

### Significant decisions get an ADR

Anything you'd want a future session to understand the reasoning behind — framework choice, data store, model provider, orchestration pattern, an API shape you picked over alternatives — gets `.project/ADR/ADR-NNN-title.md`:

```
# ADR-NNN: [Title]
**Date**: YYYY-MM-DD  **Phase**: Phase N  **Status**: Accepted

## Context
[situation/requirement that prompted this]

## Decision
[what was decided]

## Rationale
[why this over the alternatives]

## Alternatives Considered
- **[Option]**: [why rejected]

## Consequences
[what this enables, what it constrains going forward]
```

For AI/ML work specifically, always write one for: model/provider selection, embedding strategy, vector store choice, orchestration framework, and eval/prompt-versioning approach.

### AI/ML projects: keep a model registry

Normal code projects don't have this dimension, but AI/ML ones do — which model backs which component, which prompt version, which embedding config. Even if the user also uses MLflow/W&B for experiment tracking, this registry is different in kind: it's not metrics, it's the *decision trail* of what's running and why, readable without any external tool. Maintain `.project/MODEL_REGISTRY.md` (schema in `references/documentation-schema.md`), one entry per component:

```
## [Component Name]
- **Model**: name + version
- **Provider**: Anthropic | OpenAI | HuggingFace | local | other
- **Purpose**: what this model does here
- **Key config**: temperature, max_tokens, chunk_size, top_k — whatever's relevant
- **Prompt version**: vX.Y (path to the prompt file if versioned)
- **Introduced in**: Phase N
- **Rationale**: why this model for this role
- **Last updated**: YYYY-MM-DD
```

Update it the moment a model, prompt, or embedding config changes — this file goes stale fast if it's an afterthought.

## After a phase finishes: update docs before doing anything else

This is not optional cleanup — it's the mechanism that makes the next session possible at all. Do it immediately, before moving on:

1. **Append to `PHASE_LOG.md` and `.json`** — what was built, the files touched, the key decisions and their rationale (not just what you chose but what you didn't and why), any issues flagged, any dependencies or model/prompt changes introduced. Write this like you're explaining it to a colleague who wasn't in the room, because in a future session, that's exactly who's reading it.
2. **Update `PROJECT_STATE.md`/`.json`** — advance the current phase, append this session to the session history, refresh the open-issues list.
3. **Update `DEPENDENCY_MANIFEST`** and **`MODEL_REGISTRY`** if applicable.
4. **Commit**: `git add . && git commit -m "feat(phase-N): [name] — [one-line summary]"`.
5. **Report to the user**:

```
## Phase N Complete
[2-3 sentence summary]
**Files created**: [count]
**Issues flagged**: [None | list]
**Next phase**: Phase N+1 — [Name]
```

**Then pause and wait** — don't auto-start the next phase. The user may want to inspect what was built, redirect, or just stop for the day.

If a session ends *mid-phase* (context running out, user has to stop), don't skip this step — log how far you got and what's left, exactly as if the phase were its own mini-phase. An honest "got through steps 1-3 of 5, here's what remains" is far more useful to the next session than silence.

## The continuity bar

Before ending any session, ask yourself: could a brand-new Claude, with zero memory of this conversation, open `.project/PROJECT_STATE.md` right now and know (1) what this project is, (2) what's been built and where, (3) why the non-obvious decisions were made, (4) what's currently broken or open, and (5) exactly what to do next? If the answer is no, the documentation step above isn't done yet — finish it before stopping, even if that's the last thing you do in the session.
