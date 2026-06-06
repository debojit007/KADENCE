from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ResumeParts:
    name: str
    contact_line: str
    linkedin_line: str
    role: str
    summary: str
    experience_html: str
    leadership_html: str
    skills_text: str
    word_count: int
    required_sections: dict[str, bool]


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9$+/%.-]+", text)


def inline_md(text: str) -> str:
    escaped = html.escape(text.strip())
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    return escaped


def split_sections(lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = "__preamble__"
    sections[current] = []
    for line in lines:
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        else:
            sections.setdefault(current, []).append(line)
    return sections


def render_block_lines(lines: list[str]) -> str:
    out: list[str] = []
    in_ul = False
    for line in lines:
        raw = line.rstrip()
        if not raw:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            continue
        if raw.startswith("### "):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            out.append(f'<h3>{inline_md(raw[4:])}</h3>')
            continue
        if raw.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f'<li>{inline_md(raw[2:])}</li>')
            continue
        if in_ul:
            out.append("</ul>")
            in_ul = False
        # Treat company/date lines after h3 as compact metadata.
        if " · " in raw and not raw.startswith("#"):
            out.append(f'<div class="meta">{inline_md(raw)}</div>')
        else:
            out.append(f'<p>{inline_md(raw)}</p>')
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)


def parse_resume(markdown: str) -> ResumeParts:
    lines = markdown.splitlines()
    name = ""
    contact_line = ""
    linkedin_line = ""
    role = ""

    for i, line in enumerate(lines):
        if line.startswith("# ") and not name:
            name = line[2:].strip()
            contact_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            linkedin_line = lines[i + 2].strip() if i + 2 < len(lines) else ""
        if line.startswith("## "):
            role = line[3:].strip()
            break

    sections = split_sections(lines)
    summary_lines = sections.get(role, []) if role else []
    summary = " ".join(line.strip() for line in summary_lines if line.strip())

    experience_key = "Recent Professional Experience"
    if experience_key not in sections and "Professional Experience" in sections:
        experience_key = "Professional Experience"
    skills_key = "Technical Environment"
    if skills_key not in sections and "Technical Skills" in sections:
        skills_key = "Technical Skills"

    skills_text = " ".join(line.strip() for line in sections.get(skills_key, []) if line.strip())

    required = {
        "role_header": bool(role),
        "recent_professional_experience": "Recent Professional Experience" in sections,
        "leadership": "Leadership & Organizational Impact" in sections,
        "technical_skills_or_environment": skills_key in sections,
    }

    return ResumeParts(
        name=name,
        contact_line=contact_line,
        linkedin_line=linkedin_line,
        role=role,
        summary=summary,
        experience_html=render_block_lines(sections.get(experience_key, [])),
        leadership_html=render_block_lines(sections.get("Leadership & Organizational Impact", [])),
        skills_text=skills_text,
        word_count=len(words(markdown)),
        required_sections=required,
    )


def contact_items(contact_line: str, linkedin_line: str) -> str:
    chunks = [c.strip() for c in contact_line.replace("  ", " ").split("·") if c.strip()]
    icons = ["📍", "✉", "☎"]
    rows = []
    for icon, chunk in zip(icons, chunks):
        rows.append(f'<div class="contact-item"><span>{icon}</span><span>{html.escape(chunk)}</span></div>')
    if linkedin_line:
        label = linkedin_line.replace("LinkedIn:", "").strip()
        rows.append(f'<div class="contact-item"><span>🔗</span><span>{html.escape(label)}</span></div>')
    return "\n".join(rows)


def skills_items(skills_text: str) -> str:
    parts = [p.strip() for p in re.split(r"\s*·\s*", skills_text) if p.strip()]
    return "\n".join(f'<span class="skill">{inline_md(p)}</span>' for p in parts)


def html_doc(parts: ResumeParts) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(parts.name)} — Resume</title>
<style>
  :root {{ --ink:#172033; --muted:#5d6778; --line:#d9dee8; --panel:#f5f7fb; --accent:#2557a7; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:#eef1f6; color:var(--ink); font-family: Arial, Helvetica, sans-serif; font-size: 10.2pt; line-height:1.28; }}
  .page {{ width: 8.5in; min-height: 11in; margin: 0 auto; background:white; display:grid; grid-template-columns: 2.15in 1fr; box-shadow:0 8px 24px rgba(0,0,0,.12); }}
  aside {{ background:var(--panel); border-right:1px solid var(--line); padding:.34in .22in; }}
  main {{ padding:.33in .38in .28in .34in; }}
  h1 {{ margin:0 0 .04in; font-size:23pt; letter-spacing:-.4px; }}
  h2 {{ margin:.16in 0 .07in; font-size:10.8pt; text-transform:uppercase; letter-spacing:.7px; color:var(--accent); border-bottom:1px solid var(--line); padding-bottom:.025in; }}
  h3 {{ margin:.12in 0 .015in; font-size:10.8pt; color:var(--ink); }}
  p {{ margin:.04in 0 .07in; }}
  ul {{ margin:.035in 0 .08in .15in; padding:0; }}
  li {{ margin:.025in 0; padding-left:.02in; }}
  .role {{ color:var(--accent); font-weight:700; font-size:13pt; margin-bottom:.12in; }}
  .summary {{ font-size:10.2pt; }}
  .meta {{ color:var(--muted); font-size:9.2pt; margin-bottom:.035in; }}
  .contact-item {{ display:grid; grid-template-columns:.2in 1fr; gap:.05in; align-items:start; margin:.055in 0; font-size:9.2pt; word-break:break-word; }}
  .skill-list {{ display:flex; flex-wrap:wrap; gap:.05in; margin-top:.06in; }}
  .skill {{ display:inline-block; border:1px solid var(--line); border-radius:999px; padding:.025in .065in; background:white; font-size:8.7pt; }}
  strong {{ font-weight:700; }}
  code {{ font-family:inherit; }}
  @page {{ size: Letter; margin: .25in; }}
  @media print {{
    body {{ background:white; }}
    .page {{ width:auto; min-height:auto; margin:0; box-shadow:none; }}
    aside {{ break-inside:avoid; }}
    h2, h3 {{ break-after:avoid; }}
    li {{ break-inside:avoid; }}
  }}
</style>
</head>
<body>
<div class="page">
  <aside>
    <h2>Contact</h2>
    {contact_items(parts.contact_line, parts.linkedin_line)}
    <h2>Technical Skills</h2>
    <div class="skill-list">{skills_items(parts.skills_text)}</div>
  </aside>
  <main>
    <h1>{html.escape(parts.name)}</h1>
    <div class="role">{html.escape(parts.role)}</div>
    <p class="summary">{inline_md(parts.summary)}</p>
    <h2>Recent Professional Experience</h2>
    {parts.experience_html}
    <h2>Leadership &amp; Organizational Impact</h2>
    {parts.leadership_html}
  </main>
</div>
</body>
</html>
'''


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Markdown resume to compact HTML.")
    parser.add_argument("input", type=Path, help="Input Markdown resume")
    parser.add_argument("-o", "--output", type=Path, help="Output HTML path")
    args = parser.parse_args()

    markdown = args.input.read_text(encoding="utf-8")
    parts = parse_resume(markdown)
    output = args.output or args.input.with_suffix(".html")
    output.write_text(html_doc(parts), encoding="utf-8")

    print(f"source={args.input}")
    print(f"output={output}")
    print(f"word_count={parts.word_count}")
    for key, value in parts.required_sections.items():
        print(f"section_{key}={str(value).lower()}")
    print("remote_assets=false")


if __name__ == "__main__":
    main()
