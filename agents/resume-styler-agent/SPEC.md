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

When the target posting includes a company and job ID, name the HTML file as `<Candidate_Name>_<Company_Name>_<Job_ID>.html`, using underscores and no spaces.

## Layout Rules

1. Use a two-column layout for print and desktop:
   - Left rail: contact details with simple visual icons, technical skills, compact profile metadata.
   - Main panel: name, role, summary, Recent Experience or Recent Professional Experience, Leadership & Organizational Impact, Previous Experience when applicable.
2. Rename `Technical Environment` or `Targeted Skills` to `Technical Skills` in the HTML output.
3. Keep the resume role header as only the target role.
4. Preserve the approved experience section name but include the date span inline, for example `Recent Experience | 2020-2026`.
5. Use compact spacing, panels, timeline labels, and typographic hierarchy to reduce unused space.
6. Include print CSS targeting two pages.
7. Add candidate-facing contact icons without sacrificing ATS readability:
   - `📍` before location text.
   - `☎` inside a `tel:` phone hyperlink.
   - `✉` inside a `mailto:` email hyperlink.
   - `🔗` inside the LinkedIn/profile hyperlink.
8. Use real hyperlinks for phone, email, and profile URLs. Icons are decorative and must not replace readable text.
9. If the resume is under the configured word budget and still has visual whitespace, use approved source content to add compact value, commonly `Previous Experience | YYYY-YYYY`, instead of leaving avoidable empty space.

## Quality Gate

After generating HTML, report:

1. Markdown input path.
2. HTML output path.
3. Word count of source Markdown.
4. Whether required sections were found.
5. Whether any remote assets were used; this must be `false`.
6. Whether contact links include `tel:`, `mailto:`, and profile URL anchors.
7. Whether the target title is used only as the header and not repeated in every project heading.
8. Whether visible text stays under the configured word limit, default 600 words for strict two-page HTML resumes.
9. Whether stale or user-rejected terms were found.

If a required section is missing, generate best-effort HTML but mark the section check as failed.

Before delivery, run `resume-reviewer-agent` or equivalent checks against the generated artifact.
