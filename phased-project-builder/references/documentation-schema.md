# Documentation Schema Reference

JSON shape for every file in `.project/`. Each `.md` file has a `.json` sidecar carrying the same information in a form a future session can parse directly instead of re-reading prose. Keep both in sync on every update — a `.md` update without its `.json` counterpart (or vice versa) breaks the "future session can parse this programmatically" guarantee.

The values below are placeholders showing the *shape* of each field, not a real project or a recommended stack — don't let the specific field values below leak into an actual project's docs. Only the structure (field names, nesting, types) is prescriptive; fill every value in from the real project's own context.

## Table of contents
- [PROJECT_STATE.json](#project_statejson)
- [PHASE_LOG.json](#phase_logjson)
- [ISSUES.json](#issuesjson)
- [DEPENDENCY_MANIFEST.json](#dependency_manifestjson)
- [MODEL_REGISTRY.json](#model_registryjson)

## PROJECT_STATE.json

The front door — read first on every resume.

```json
{
  "project_name": "<the project's name, from its context files>",
  "project_type": "<e.g. AI/ML - Agentic RAG, Web App, Data Pipeline>",
  "core_goal": "<one sentence describing what this system does>",
  "status": "in_progress",
  "created_date": "<YYYY-MM-DD>",
  "last_updated": "<YYYY-MM-DD>",
  "current_phase": 2,
  "phase_plan": [
    {
      "phase": 1,
      "name": "<phase name>",
      "status": "complete",
      "depends_on": null
    },
    {
      "phase": 2,
      "name": "<phase name>",
      "status": "in_progress",
      "depends_on": 1
    }
  ],
  "session_history": [
    {
      "session": 1,
      "date": "<YYYY-MM-DD>",
      "summary": "<one-line summary of what this session did>"
    }
  ],
  "open_issues": ["ISSUE-001"]
}
```

## PHASE_LOG.json

Append-only. Never rewrite past entries — if a later phase reveals an earlier decision was wrong, add a new entry noting the correction; don't edit history.

```json
{
  "phases": [
    {
      "phase": 1,
      "name": "<phase name>",
      "date": "<YYYY-MM-DD>",
      "status": "complete",
      "summary": "<2-3 sentences on what was built and why it matters>",
      "files": [
        { "path": "<relative/path/to/file>", "description": "<what it does, one line>" }
      ],
      "decisions": [
        {
          "decision": "<what was chosen>",
          "rationale": "<why this over the alternatives, tied to something in the project's own context files>"
        }
      ],
      "issues_flagged": ["ISSUE-001"],
      "dependencies_added": [
        { "package": "<name==version>", "reason": "<why it's needed>" }
      ],
      "model_registry_changes": ["<one-line pointer to what changed, if this is an AI/ML project>"]
    }
  ]
}
```

## ISSUES.json

```json
{
  "issues": [
    {
      "id": "ISSUE-001",
      "title": "<short descriptive title>",
      "phase": 1,
      "severity": "Warning",
      "description": "<what's wrong, specifically>",
      "context": "<what was happening when this was found>",
      "impact": "<what can't proceed, or what risk this carries, until resolved>",
      "suggested_resolution": "<best read on what to do>",
      "status": "Open",
      "date": "<YYYY-MM-DD>"
    }
  ]
}
```

Severity guide: **Blocker** — stop and wait for the user before continuing this phase. **Warning** — can proceed but must be surfaced and tracked, since it'll likely bite later. **Note** — worth recording, doesn't block anything.

## DEPENDENCY_MANIFEST.json

```json
{
  "dependencies": [
    {
      "package": "<name==version>",
      "phase_introduced": 1,
      "reason": "<why it's needed>"
    }
  ]
}
```

## MODEL_REGISTRY.json

AI/ML projects only. This is a decision trail, not a metrics dashboard — even projects already using MLflow/W&B for experiment metrics should keep this, since it answers "what's running and why" without needing to open another tool.

```json
{
  "components": [
    {
      "name": "<component name, e.g. Document Embedder, Response Synthesizer>",
      "model": "<model name and version>",
      "provider": "<Anthropic | OpenAI | HuggingFace | local | other>",
      "purpose": "<what this model does in the system>",
      "key_config": { "<param>": "<value>" },
      "prompt_version": "<version, or null if not applicable>",
      "introduced_in_phase": 1,
      "rationale": "<why this model for this role, tied to something in the project's own context files>",
      "last_updated": "<YYYY-MM-DD>"
    }
  ]
}
```
