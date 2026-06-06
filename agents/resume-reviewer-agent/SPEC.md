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
2. Markdown experience section is titled `Recent Professional Experience`, not `Professional Experience`.
3. HTML output uses `Technical Skills`, not `Technical Environment`.
4. Project headings do not repeat the target role/title.
5. No duplicate bold metrics in Markdown.
6. No repeated 4-6 word phrases in Markdown, excluding unavoidable headings/contact text.
7. Markdown stays at or under the configured word limit, default 600 words.
8. HTML contains no remote assets, scripts, external fonts, links, CSS imports, or CSS `url(...)` references.
9. HTML preserves source metrics from Markdown when both files are provided.

## Output

Print a concise review report with PASS/FAIL per check and an overall status. The reviewer must not mutate artifacts.
