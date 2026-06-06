# Final Resume Quality Gate

Use this gate before any final resume is delivered or saved.

## Hard Length Rule

1. Final resumes must be printable as **exactly 2 pages** unless the user explicitly requests a different length.
2. A resume that prints to 3+ pages fails the gate and must be revised before delivery.
3. Use a strict compact Markdown budget of **600 words maximum** when no renderer is available. Preferred range is **500-600 words**.
4. If PDF/print tooling is available, render or print-preview the resume and verify the page count directly.
5. If the page count cannot be verified by tooling, state that the Markdown is two-page-targeted and ask the user to confirm print output.

## Mandatory Length Check After Final Actions

After every final action that creates, updates, saves, renders, or delivers a resume, immediately run a document length check before responding.

The length check must report:

1. Word count.
2. Line count.
3. Whether it fits the current page target.
4. If PDF/print tooling is available, rendered page count.
5. If rendered page count is unavailable, whether the Markdown is within the conservative 2-page budget.

For default 2-page resumes, use these guardrails when print rendering is unavailable:

- Hard maximum: **600 words**.
- Preferred range: **500-600 words**.
- Target: **45-55 lines**.
- Anything above 600 words fails the final quality gate and must be compressed before final delivery unless the user explicitly approves the overage.

Never finish a final resume action without reporting the length check result.

## Content Compression Rules

1. Remove standalone **Core Strengths** / generic skills sections by default for senior resumes.
2. Merge only role-critical keywords into the summary, experience bullets, and technical environment.
3. Preserve the strongest quantified outcomes first; delete secondary explanation before deleting impact metrics.
4. Prefer fewer, denser bullets over many thin bullets.
5. Keep senior-manager resumes focused on scope, ambiguity, cross-team influence, operating mechanisms, and business outcomes.

## Section Naming Rule

Use `## Recent Professional Experience` instead of `## Professional Experience` for tailored resumes. The section should emphasize recent, role-relevant work rather than attempting to list every job.

## Duplication Check

Before final output, scan for repetition and remove or merge duplicates:

1. Each metric should appear once unless it supports a materially different claim.
2. Each project capability should appear once; repeated keywords are allowed only when they add new evidence.
3. Do not repeat the same claim in summary, experience, leadership, and skills sections.
4. Merge overlapping leadership bullets into one stronger org-level statement.
5. Avoid repeated phrases such as "zero-to-one", "deduplication", "platform", "stakeholder alignment", and "operational excellence" unless the repeated use is necessary for ATS matching and the sentence adds distinct context.

## Final Checklist

- Page target: exactly 2 pages.
- Header check: the resume role header is only the target role, with no job-post link summary, job URL, company-specific tagline, or role-fit explanation.
- Section naming check: experience section is titled `Recent Professional Experience`.
- Heading check: project/experience headings do not repeat the candidate's role/title; use company, domain, product, or initiative names instead.
- Timeline check: experience sections use extracted company/title/date information when available; placeholders remain only when the user has not provided or confirmed reliable timeline data.
- No standalone Core Strengths section unless explicitly approved.
- No duplicated bullets, metrics, claims, or project themes.
- Every retained bullet either proves job fit, shows senior leadership scope, or quantifies business impact.
- Final resume remains truthful to the applicant facts and excludes unapproved inferred claims.
