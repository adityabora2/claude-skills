# phased-project-builder

A Claude Code skill for building a production or enterprise-grade project from a set of spec files, in small approved phases instead of one long run.

## What it does

You put your requirement and spec files (notes, architecture docs, anything in .md or plain text) into a `project-context/` folder and invoke the skill. It reads everything, summarizes the project, and proposes a phase-by-phase build plan. It waits for your approval before writing any code. Once approved, it builds one phase at a time, and after every phase it updates a set of documentation files describing what was built and why.

If it hits something broken, ambiguous, or contradictory while building, it stops and asks instead of guessing. If a new chat session is started later, it detects the existing project state and resumes exactly where it left off, without you needing to re-explain anything.

## Files

- `SKILL.md`: the skill itself.
- `references/phase-planning-guide.md`: starting phase breakdowns for a few common project types (agentic or RAG systems, multi-agent orchestration, web apps, data pipelines).
- `references/documentation-schema.md`: the file format for the tracking documents the skill creates.

## Installing

Copy this folder into your skills directory:

```bash
cp -r phased-project-builder ~/.claude/skills/
```

Start a new Claude Code session afterward.

## Using it

This skill only activates when you name it directly. Example:

"I put my spec files in project-context/. Use phased-project-builder to get started."

## Notes

This skill assumes tool access to read and write files, run shell commands, and use git. It was built and tested for Claude Code and has not been verified in more limited tool environments.
