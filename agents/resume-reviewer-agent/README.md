# Resume Reviewer Agent

`resume-reviewer-agent` performs deterministic final-artifact checks for Markdown and HTML resumes.

It is intended to cross-check output from `resume-agent` and `resume-styler-agent` before delivery so debug metadata, repeated claims, wrong section names, role repetition, remote assets, or length violations do not leak into final artifacts.

See [SPEC.md](SPEC.md).
