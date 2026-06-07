# KADENCE

KADENCE is a monorepo for agent-first AI systems. Each agent is a self-contained workflow with typed inputs, auditable outputs, CLI access, and a future-ready API boundary.

The first agent in this repo is `resume-agent`, a workflow for generating tailored Markdown resumes from structured applicant data and a job advert URL or fallback job description text.

## Repository Model

KADENCE is organized around reusable agent infrastructure and independently testable agent modules.

```text
KADENCE/
  agents/       Agent implementations and agent-specific specs
  packages/     Shared libraries for core agent behavior and harness tooling
  skills/       Reusable agent instructions and operating patterns
  harness/      Fixtures, replay cases, validation, and eval scenarios
  apps/         Future product/API surfaces
  docs/         Architecture, contracts, and decisions
```

<!-- agentic-readme:start -->
## Current Agents

This section is maintained by the local agentic pre-commit hook from `agent-registry.json`.

| Agent | Status | Purpose |
| --- | --- | --- |
| `resume-agent` | Spec | Generate tailored ATS-friendly Markdown resumes with mandatory review and audit logging |
| `resume-styler-agent` | Local deterministic renderer | Convert approved Markdown resumes into compact local-only print-ready HTML |
| `resume-reviewer-agent` | Local deterministic reviewer | Run deterministic final-artifact checks for Markdown and HTML resumes |

## Agentic Commit Hook

KADENCE includes a local pre-commit hook that runs `scripts/update_readme.py` before each commit. The hook refreshes this README from local repository metadata and stages `README.md` when it changes, so commits include the latest project overview.
<!-- agentic-readme:end -->

## Resume Agent Flow

```text
  Applicant Profile JSON              Job Advert URL
          |                                  |
          v                                  v
  +------------------+              +------------------+
  | Validate Profile |              | Fetch Job Advert |
  +------------------+              +------------------+
          |                                  |
          |                         if fetch fails
          |                                  v
          |                       Fallback Job Text
          |                                  |
          +---------------+------------------+
                          |
                          v
                +--------------------+
                | Normalize Job Data |
                +--------------------+
                          |
                          v
                +--------------------+
                | Draft Resume Claims|
                +--------------------+
                          |
                          v
                +--------------------+
                | Mandatory Review  |
                | Human / Agent /   |
                | Event Response    |
                +--------------------+
                          |
                 approved or edited
                          |
                          v
                +--------------------+
                | Render Markdown   |
                | Resume Artifact   |
                +--------------------+
                          |
                          v
              resume.md + append-only audit log
```

## Design Principles

1. Agent-first interfaces before UI.
2. Typed JSON contracts for inputs, intermediate artifacts, and outputs.
3. Required audit trails for every consequential workflow step.
4. Human or agent review before final artifacts are produced.
5. Minimal dependencies until complexity justifies additional framework weight.
6. Shared infrastructure belongs in `packages/`; agent-specific behavior belongs in `agents/`.

## Recommended Stack

- Python 3.12+
- `uv` workspace
- Pydantic for schemas and validation
- Typer for CLI entrypoints
- OpenAI as the default configurable LLM provider
- FastAPI later as an API wrapper around the core workflow
- Append-only JSONL event logs for audit

## First Implementation Target

See [agents/resume-agent/SPEC.md](agents/resume-agent/SPEC.md).
