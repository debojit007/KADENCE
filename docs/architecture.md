# KADENCE Architecture

KADENCE is a directory-per-agent monorepo. Each agent owns its workflow, schemas, prompts, examples, and tests. Shared behavior lives in packages so future agents can reuse audit logging, LLM provider adapters, artifact handling, review gates, and harness utilities.

## Top-Level Areas

```text
agents/   Actual agent implementations
packages/ Shared libraries used by agents and harnesses
skills/   Reusable agent instructions and operating patterns
harness/  Fixtures, replay, validation, and evaluation cases
apps/     Future product and API surfaces
docs/     Contracts, architecture, and decisions
```

## Runtime Shape

The first implementation target should be a Python `uv` workspace:

1. `packages/kadence-core` provides reusable primitives.
2. `packages/kadence-harness` provides test and replay tooling.
3. `agents/resume-agent` provides the first concrete agent.
4. `apps/api` can later wrap agent workflows with FastAPI.

## Agent Workflow Contract

Every agent should define:

1. Typed input schema.
2. Typed output schema.
3. Explicit workflow states.
4. CLI entrypoint.
5. Audit event model.
6. Review or approval gates where needed.
7. Harness cases with deterministic validation.

