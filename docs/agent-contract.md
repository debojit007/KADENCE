# Agent Contract

Every KADENCE agent must be callable by a human operator, Codex, another automated agent, or a future API wrapper.

## Required Files

```text
agents/{agent-name}/
  SPEC.md
  README.md
  pyproject.toml
  src/
  schemas/
  prompts/
  examples/
  tests/
  skills/
```

## Required Capabilities

1. Validate structured input before calling an LLM.
2. Produce structured intermediate artifacts.
3. Record every consequential step in an append-only audit log.
4. Stop at review gates instead of silently finalizing risky outputs.
5. Render final artifacts from approved structured data.
6. Provide harness cases for replay and regression testing.

## Interface Preference

The preferred v1 interface is:

1. Core library.
2. CLI wrapper.
3. API wrapper later.

This keeps agents easy for Codex and other automation systems to call while preserving a direct path to web-app integration.

