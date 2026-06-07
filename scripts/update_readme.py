#!/usr/bin/env python3
"""Regenerate README sections from local KADENCE agent metadata.

This is intentionally deterministic and local-only so it can run from a Git
pre-commit hook without external services or paid API calls.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
REGISTRY = ROOT / "agent-registry.json"

START = "<!-- agentic-readme:start -->"
END = "<!-- agentic-readme:end -->"

STATUS_LABELS = {
    "spec": "Spec",
    "local-renderer": "Local deterministic renderer",
    "local-reviewer": "Local deterministic reviewer",
}

PURPOSES = {
    "resume-agent": "Generate tailored ATS-friendly Markdown resumes with mandatory review and audit logging",
    "resume-styler-agent": "Convert approved Markdown resumes into compact local-only print-ready HTML",
    "resume-reviewer-agent": "Run deterministic final-artifact checks for Markdown and HTML resumes",
}


def load_agents() -> list[dict]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return data.get("agents", [])


def render_agentic_section() -> str:
    agents = load_agents()
    rows = []
    for agent in agents:
        agent_id = agent["id"]
        status = STATUS_LABELS.get(agent.get("status", ""), agent.get("status", ""))
        purpose = PURPOSES.get(agent_id, ", ".join(agent.get("capabilities", [])))
        rows.append(f"| `{agent_id}` | {status} | {purpose} |")

    return "\n".join(
        [
            START,
            "## Current Agents",
            "",
            "This section is maintained by the local agentic pre-commit hook from `agent-registry.json`.",
            "",
            "| Agent | Status | Purpose |",
            "| --- | --- | --- |",
            *rows,
            "",
            "## Agentic Commit Hook",
            "",
            "KADENCE includes a local pre-commit hook that runs `scripts/update_readme.py` before each commit. The hook refreshes this README from local repository metadata and stages `README.md` when it changes, so commits include the latest project overview.",
            END,
        ]
    )


def replace_section(text: str, generated: str) -> str:
    if START in text and END in text:
        before = text.split(START, 1)[0].rstrip()
        after = text.split(END, 1)[1].lstrip()
        return f"{before}\n\n{generated}\n\n{after}".rstrip() + "\n"

    current_agents = text.find("## Current Agents")
    resume_flow = text.find("## Resume Agent Flow")
    if current_agents == -1 or resume_flow == -1 or resume_flow < current_agents:
        return text.rstrip() + "\n\n" + generated + "\n"

    before = text[:current_agents].rstrip()
    after = text[resume_flow:].lstrip()
    return f"{before}\n\n{generated}\n\n{after}".rstrip() + "\n"


def main() -> int:
    original = README.read_text(encoding="utf-8")
    updated = replace_section(original, render_agentic_section())
    if updated != original:
        README.write_text(updated, encoding="utf-8")
        print("README.md updated from agent-registry.json")
    else:
        print("README.md already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
