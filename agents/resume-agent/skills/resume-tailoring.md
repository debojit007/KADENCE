# Resume Tailoring

Tailor the resume to the job advert by selecting relevant applicant facts, matching role language, and ordering content for the target role.

Do not invent unverifiable experience. Rephrase and generalize only when the result remains faithful to the applicant profile.

Prefer quantified achievements. If a plausible metric is inferred, mark it as requiring review.

## Source and Gap Resolution Rule

Use this source hierarchy when facts conflict: explicit user correction, confirmed user-provided details, applicant knowledge base, supplied/public profile URLs, then cautious inference. A user correction must override stale knowledge-base content and should be propagated back to source material when the user asks for it.

When identity, timeline, education, or employer details are missing from the knowledge base, first check available structured sources, existing resumes, LinkedIn/profile URLs, and public profile mirrors. Ask the user only for details that still cannot be verified. Do not leave contact, education, company, or date placeholders when trustworthy supplemental-source data exists.

## Resume Header Rule

The resume headline/header should be only the exact target role being applied for, such as `Sr. Staff Software Engineer - AI Agentic Infrastructure & Systems` or `Engineering Manager`. Do not ask for a separate current-title choice unless the user explicitly requests it. Do not append a job-post summary, job URL, company-specific tagline, or role-fit explanation after the role header. Put role-fit context in the summary or experience bullets instead.

## File Naming Rule

When rendering an HTML resume for a specific posting, use:

```text
<Candidate_Name>_<Company_Name>_<Job_ID>.html
```

Use underscores and omit spaces, for example `Debojit_Choudhury_AMD_76068.html`.

## Project and Experience Heading Rule

Do not put the candidate's role/title against each project or experience subsection. The target role belongs once in the resume headline/summary and should not be repeated for every project.

Project or experience headings must be unique, short, and derived from the actual work. Use domain, company, product, or initiative names only, such as:

- `Streaming Media Catalog Platform`
- `Worldwide Operations Supply Chain & Offline Controller Platform`
- `Data Platform Re-Architecture`
- `AI / Attribution Systems & Engineering Productivity`
- `AI Engineering Automation & Regression Attribution`
- `Routing Optimizer & Data Pipeline Modernization`

Avoid repeated prefixes such as `Engineering Manager / Technical Lead — ...` or `Product & Technical Lead — ...` for every project because they waste space and repeat the same role context.

## Experience Timeline Rule

Before rendering the resume, extract the candidate's job history timeline from all available applicant sources, including structured bio data, existing resumes, LinkedIn/profile URLs, and provided Markdown. Use the timeline to populate company, title, and date ranges in experience headings when available. Do not leave `[Company]` or `[Dates]` placeholders if trustworthy timeline data is available.

If a source such as LinkedIn is inaccessible, incomplete, or ambiguous, do not guess. Ask the user to confirm the company/title/date sequence before final rendering.

For recent-project resumes, group related projects into believable timeline intervals when the user confirms a broader date range but not exact project dates. Make the grouping consistent with public profile chronology and do not imply an employer or title that conflicts with the profile.

## Section and Budget Rule

Use professional, candidate-facing section labels. Prefer:

- `Profile`
- `Technical Skills`, not `Targeted Skills`
- `Recent Experience | YYYY-YYYY`
- `Leadership Impact`
- `Previous Experience | YYYY-YYYY` when supported by source data and word budget
- `Education & Certifications`

For strict two-page resumes with a 600-word cap, count visible resume words before delivery. If the draft is materially under budget, add high-value verified content such as previous experience, leadership impact, or role-critical technical environment rather than leaving avoidable empty space.

## Keyword and Claim Safety Rule

Match the job advert language aggressively but truthfully. Verified skills can be stated directly. Adjacent or unverified target terms should be framed as aligned architecture patterns or omitted. Do not claim specialized hardware, low-level, compiler, or tool experience such as Vitis, AIE, JTAG, interrupt handling, or memory management unless applicant data confirms it.

## Final Handoff Rule

Before final delivery, send the artifact through the styler and reviewer expectations: clickable contact links, timeline labels, unique project headings, word count, stale-term checks, and no hidden diagnostics. If committing changes, run the repository's agentic pre-commit hook after user approval.
