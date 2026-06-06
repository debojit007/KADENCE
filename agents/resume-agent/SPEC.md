# Resume Agent Spec

## Status

Spec only. Do not implement until reviewed.

## Purpose

Given structured applicant data and either a job advert URL or fallback job description text, generate an ATS-friendly Markdown resume through a mandatory review and approval workflow.

The agent must be usable by:

1. A human operating through Codex.
2. Another automated agent.
3. A future web app backend.

## Framework Prescription

Use:

1. Python 3.12+.
2. Pydantic for typed models and JSON Schema generation.
3. Typer for the first CLI interface.
4. OpenAI as the default configurable LLM provider.
5. A small provider adapter to support other LLMs later.
6. Trafilatura or equivalent extraction tooling for job advert pages.
7. FastAPI later as a wrapper around the core workflow.
8. Append-only JSONL for audit events.

Do not start with a heavy agent framework. Keep the core workflow explicit and inspectable.

## Input Contract

Canonical input is JSON only.

```json
{
  "applicant_profile": {},
  "job_advert_url": "https://example.com/job",
  "job_description_text": null,
  "generation_policy": {
    "allow_inference": true,
    "require_metrics": true,
    "mark_unverified_metrics_for_review": true,
    "tone": "confident_but_not_oversold",
    "output_format": "markdown"
  }
}
```

The job advert URL is primary. If scraping fails or the site blocks access, the workflow must require manually supplied `job_description_text`.

## Applicant Profile

The applicant profile should be structured JSON, not a raw resume.

The model should support:

1. Identity and contact fields.
2. Target roles.
3. Work experience.
4. Projects.
5. Skills.
6. Education.
7. Certifications.
8. Links.
9. Resume constraints.

Achievements should be represented as structured facts whenever possible.

## Output Contract

The final resume artifact is Markdown.

Markdown is preferred because it is token-efficient, diffable, agent-friendly, easy to review, and can later be converted to PDF, HTML, or DOCX by deterministic tooling.

The LLM should generate structured intermediate artifacts. The final Markdown should be rendered from approved structured data.

By default, the final resume is a **strict two-page artifact**. It must not be delivered if it prints to 3+ pages. When PDF/print tooling is available, the render flow must verify the resume prints as exactly 2 pages. When tooling is unavailable, the agent must apply a conservative Markdown budget, typically 800-900 words and 50-65 lines, and mark the page count as requiring human print confirmation.

The final resume must pass a duplication check. Repeated claims, metrics, project themes, and generic skills sections must be merged or removed. Standalone `Core Strengths` sections should be omitted by default and role-critical keywords should be merged into the summary, experience bullets, and technical environment.

## Grounding and Claim Policy

The agent may infer, rephrase, and generalize to match the job advert. However, every strong claim must be grounded in applicant data or explicitly flagged for review.

Every resume bullet should include:

```json
{
  "text": "Improved onboarding workflow efficiency by 28% through automated validation and clearer release checklists.",
  "source_profile_refs": ["experience.2.achievements.0"],
  "job_requirement_refs": ["job.requirements.3"],
  "metric_status": "verified",
  "review_status": "pending"
}
```

Allowed `metric_status` values:

1. `verified`
2. `inferred_needs_review`
3. `missing`

The final resume must not include rejected claims.

## Required Review Gate

The workflow must always pause for review before final rendering.

The reviewer can be:

1. A human.
2. Another agent.
3. A response to an event.

The draft phase must produce:

```text
claims_review.json
resume_draft.json
final_quality_review.json
```

The render phase must require an approved or edited review decision and an approved final quality review covering page count, duplicate content, and rejected/inferred claims.

## Workflow States

```text
CREATED
  -> JOB_READY
  -> DRAFT_READY
  -> REVIEW_PENDING
  -> APPROVED or CHANGES_REQUESTED
  -> FINAL_RENDERED
```

## Audit

Use a local append-only JSONL event log in v1.

Example run layout:

```text
runs/{run_id}/
  events.jsonl
  inputs/
    applicant_profile.json
    job_advert.txt
  drafts/
    resume_draft.json
    claims_review.json
    final_quality_review.json
  final/
    resume.md
```

Each audit event should record:

1. Timestamp.
2. Run id.
3. Actor type.
4. Event type.
5. Artifact path.
6. Artifact hash.
7. LLM provider and model when applicable.
8. Token usage when available.
9. Cost estimate when available.
10. Error details when applicable.

Generated runs should be ignored by git because they may contain applicant PII.

## CLI Surface

Target v1 commands:

```bash
kadence-resume init-run --profile applicant.json --job-url "https://example.com/job"
kadence-resume init-run --profile applicant.json --job-text job.txt
kadence-resume draft --run runs/abc123
kadence-resume review --run runs/abc123 --decision review.json
kadence-resume render --run runs/abc123
```

The `draft` command must stop at review. It must not silently produce the final resume.

## Future API Surface

FastAPI can later expose:

```text
POST /runs
POST /runs/{id}/draft
GET  /runs/{id}/review
POST /runs/{id}/review
POST /runs/{id}/render
GET  /runs/{id}/artifacts/resume.md
```

The API must call the same core workflow as the CLI.

## Proposed Package Layout

```text
agents/resume-agent/
  README.md
  SPEC.md
  pyproject.toml
  src/kadence_resume_agent/
    cli.py
    workflow.py
    models/
      applicant.py
      job.py
      draft.py
      review.py
      audit.py
    ingest/
      job_advert.py
    llm/
      base.py
      openai_provider.py
    render/
      markdown.py
    audit/
      event_log.py
  schemas/
  prompts/
  examples/
  tests/
  skills/
    SKILL.md
    resume-tailoring.md
    claim-review.md
```

## Harness Cases

Initial harness cases should include:

1. Successful job URL extraction.
2. Blocked job URL with fallback job text.
3. Applicant profile missing metrics.
4. Reviewer rejects inferred claims.
5. Reviewer edits claims before final rendering.

## Non-Goals For V1

1. PDF generation.
2. Web app UI.
3. Raw resume PDF parsing as the primary input.
4. Database-backed persistence.
5. Multi-agent orchestration framework.
6. Automatic application submission.
