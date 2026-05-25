# KADENCE Harness

The harness contains reusable fixtures, replay inputs, validation rules, and reports for KADENCE agents.

Reports are ignored by git by default.

## Planned Commands

```bash
kadence-harness run resume-agent --case basic-software-engineer
kadence-harness replay --run runs/abc123
kadence-harness validate-audit --run runs/abc123
kadence-harness compare --case basic-software-engineer --run runs/abc123
```

