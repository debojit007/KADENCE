# Resume Reviewer Agent Spec

## Status

Local deterministic reviewer.

## Purpose

Cross-check final resume artifacts produced by other agents before delivery.

## Inputs

One or both of:

1. Markdown resume path.
2. HTML resume path.

## Checks

1. No visible or hidden diagnostic/generation metadata in final artifacts, including source paths, word-count notes, remote-asset notes, section booleans, debug strings, or reviewer notes.
2. Experience section uses the approved recent-experience label, such as `Recent Experience | YYYY-YYYY` or `Recent Professional Experience | YYYY-YYYY`, not generic `Professional Experience`.
3. HTML output uses `Technical Skills`, not `Technical Environment` or `Targeted Skills`.
4. Project headings do not repeat the target role/title and are unique, short, and substance-derived.
5. No duplicate bold metrics in Markdown.
6. No repeated 4-6 word phrases in Markdown, excluding unavoidable headings/contact text.
7. Markdown and HTML visible text stay at or under the configured word limit, default 600 words for strict two-page resumes.
8. HTML contains no remote assets, scripts, external fonts, CSS imports, or CSS `url(...)` references. Normal candidate hyperlinks such as `tel:`, `mailto:`, and LinkedIn/profile URLs are allowed.
9. HTML preserves source metrics from Markdown when both files are provided.
10. HTML filename follows `<Candidate_Name>_<Company_Name>_<Job_ID>.html` when company and job ID are known.
11. Contact row contains readable location, phone, email, and profile text with `tel:`, `mailto:`, and URL anchors when those inputs are available.
12. Header role matches the target job title, with role-fit context placed in summary or bullets rather than appended to the header.
13. Stale or user-rejected source terms are absent, for example `DocumentDB` after the user corrected the vector store to `OpenSearch`.
14. Job keywords are truthful: verified skills are direct, adjacent/unverified target terms are clearly framed as aligned patterns or omitted.
15. If the resume is far below the configured budget and has obvious whitespace, warn that a supported `Previous Experience` or leadership-impact section should be considered.

## Agentic Pre-Commit Hook

Before repository commits that change resume agents, resume artifacts, docs, or generated metadata, run the repository's agentic pre-commit hook after user approval. The hook may update and stage generated files such as `README.md`; include those changes in the final review scope. If the hook is unavailable, run the reviewer checks manually and report that the hook was skipped.

## Output

Print a concise review report with PASS/FAIL per check and an overall status. The reviewer must not mutate artifacts.
