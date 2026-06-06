# Resume Agent

`resume-agent` is the first KADENCE agent.

It generates tailored ATS-friendly Markdown resumes from structured applicant data and a job advert URL or fallback job description text.

The workflow must always include a review step before producing the final resume.

Final resumes must also pass a quality gate: exactly 2 printed pages by default, no repeated claims/metrics/themes, and no standalone generic skills section unless explicitly approved.

See [../../agents/resume-agent/SPEC.md](../../agents/resume-agent/SPEC.md).
