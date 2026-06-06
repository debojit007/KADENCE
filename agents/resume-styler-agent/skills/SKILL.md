# Resume Styler Agent Skill

Use this skill when converting a Markdown resume into print-ready HTML.

## Operating Rules

1. Take a Markdown resume as input and produce a standalone HTML file.
2. Preserve facts, metrics, and claims; do not invent, expand, or rewrite content beyond light heading normalization.
3. Use a two-column layout: left rail for contact details and `Technical Skills`, main panel for summary, `Recent Professional Experience`, and leadership sections.
4. Rename `Technical Environment` to `Technical Skills` in the HTML output.
5. Do not use remote assets, external fonts, scripts, trackers, or paid APIs.
6. Prefer Unicode/CSS icons for contact visuals.
7. Include print CSS that targets a compact two-page resume.
8. Never embed diagnostics, source paths, word counts, remote-asset status, reviewer notes, debug strings, or generation metadata in the final HTML. Report those only in CLI stdout or a separate report.
9. After generation, report source path, output path, word count, required section checks, and remote asset status.
10. Before delivery, run `resume-reviewer-agent` or equivalent checks against the generated artifact.
