# Resume Styler Agent Spec

## Status

Local deterministic renderer.

## Purpose

Convert a tailored Markdown resume into a compact, print-friendly HTML resume without inventing, expanding, or changing factual claims.

## Input

A Markdown resume file generated or approved by `resume-agent`.

## Output

A standalone `.html` file containing all CSS inline. The output must use local-only assets: no remote fonts, images, scripts, trackers, or paid API calls.

Final HTML must contain only candidate-facing resume content. Diagnostics such as word counts, section-check booleans, remote-asset status, source paths, reviewer notes, debug strings, or generation metadata must be reported only through CLI stdout or a separate report, never embedded as visible or hidden content in the resume HTML.

## Layout Rules

1. Use a two-column layout for print and desktop:
   - Left rail: contact details with simple visual icons, technical skills, compact profile metadata.
   - Main panel: name, role, summary, Recent Professional Experience, Leadership & Organizational Impact.
2. Rename `Technical Environment` to `Technical Skills` in the HTML output.
3. Keep the resume role header as only the target role.
4. Preserve `Recent Professional Experience` as the experience section name.
5. Use compact spacing, panels, timeline labels, and typographic hierarchy to reduce unused space.
6. Include print CSS targeting two pages.

## Quality Gate

After generating HTML, report:

1. Markdown input path.
2. HTML output path.
3. Word count of source Markdown.
4. Whether required sections were found.
5. Whether any remote assets were used; this must be `false`.

If a required section is missing, generate best-effort HTML but mark the section check as failed.

Before delivery, run `resume-reviewer-agent` or equivalent checks against the generated artifact.
