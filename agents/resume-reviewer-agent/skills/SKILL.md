# Resume Reviewer Agent Skill

Use this skill when reviewing final Markdown or HTML resume artifacts before delivery.

## Operating Rules

1. Review artifacts only; do not mutate them.
2. Check that final artifacts contain only candidate-facing resume content.
3. Fail any artifact containing diagnostics, generation metadata, source paths, word-count notes, remote-asset notes, debug strings, section booleans, or reviewer notes.
4. Verify resume-agent conventions: `Recent Professional Experience`, role-only header, no role/title repeated in project headings, no standalone `Core Strengths` unless explicitly approved.
5. Verify styler-agent conventions: HTML uses `Technical Skills`, has contact and skills panels, contains no remote assets/scripts/fonts/imports, and preserves source metrics.
6. Verify length: default Markdown limit is 600 words unless the user explicitly approved a different limit.
7. Report PASS/FAIL per check and overall status before final delivery.
