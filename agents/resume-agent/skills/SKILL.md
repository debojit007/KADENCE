# Resume Agent Skill

Use this skill when the task is to generate or review a tailored resume from structured applicant data and a job advert.

## Operating Rules

1. Prefer structured applicant facts over raw resume text.
2. Use the job advert URL first and fallback text when scraping fails.
3. Generate structured draft claims before Markdown.
4. Flag inferred metrics for review.
5. Always stop for review before final rendering.
6. Render final Markdown only from approved or edited claims.
7. Record all consequential actions in the audit log.

