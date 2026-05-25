# ADR-0001: Directory-Per-Agent Monorepo

## Status

Accepted.

## Context

KADENCE will contain many agent-first systems. Each agent needs its own workflow, schemas, prompts, examples, tests, and future deployment path. Shared primitives should not be copied across agents.

## Decision

Use a directory-per-agent monorepo on the main branch:

```text
agents/{agent-name}
packages/{shared-package}
skills/
harness/
apps/
docs/
```

Use a Python `uv` workspace so shared packages and agent packages can be developed together with one lockfile.

## Consequences

1. Agents remain discoverable on the main branch.
2. Shared code can evolve in `packages/`.
3. CI can test one agent or the entire workspace.
4. Future APIs and web apps can wrap existing agent workflows without moving code.

