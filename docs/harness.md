# Harness

The KADENCE harness is the black-box runner and validation layer for agents.

It should let a human, Codex, CI, or another agent run the same scenario and inspect comparable outputs.

## Responsibilities

1. Run fixture-based agent cases.
2. Replay prior runs from audit logs.
3. Validate artifact shapes.
4. Validate required audit events.
5. Compare outputs against expected review structures.
6. Produce reports that are ignored by git by default.

## Target Commands

```bash
kadence-harness run resume-agent --case basic-software-engineer
kadence-harness replay --run runs/abc123
kadence-harness validate-audit --run runs/abc123
kadence-harness compare --case basic-software-engineer --run runs/abc123
```

