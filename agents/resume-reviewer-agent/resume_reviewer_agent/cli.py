from __future__ import annotations

import argparse
import html as html_lib
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


BANNED_ARTIFACT_PATTERNS = [
    r"Source words\s*:",
    r"Remote assets\s*:",
    r"remote_assets\s*=",
    r"section_[a-z0-9_]+\s*=",
    r"word_count\s*=",
    r"source\s*=.+\.md",
    r"output\s*=.+\.html",
    r"debug",
    r"diagnostic",
    r"reviewer note",
]

ROLE_PREFIX_RE = re.compile(
    r"^###\s+(Engineering Manager|Technical Lead|Product & Technical Lead|Engineering Manager /|Product Manager|Manager)\b",
    re.I,
)


@dataclass
class Check:
    name: str
    passed: bool
    detail: str


def read(path: Path | None) -> str:
    return path.read_text(encoding="utf-8") if path else ""


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9$+/%.-]+", text)


def strip_html(text: str) -> str:
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<script\b.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return html_lib.unescape(re.sub(r"\s+", " ", text)).strip()


def banned_metadata_check(name: str, text: str) -> Check:
    hits = []
    for pattern in BANNED_ARTIFACT_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            hits.append(pattern)
    return Check(name, not hits, "no banned metadata" if not hits else "matched: " + ", ".join(hits))


def duplicate_metrics_check(md: str) -> Check:
    metrics = extract_bold_metrics(md)
    dupes = {k: v for k, v in Counter(metrics).items() if v > 1}
    return Check("markdown_duplicate_bold_metrics", not dupes, "none" if not dupes else str(dupes))


def extract_bold_metrics(md: str) -> list[str]:
    return [m for m in re.findall(r"\*\*(.+?)\*\*", md, flags=re.S) if re.search(r"\d|\$", m)]


def repeated_phrases_check(md: str) -> Check:
    tokens = [w.lower() for w in words(md)]
    repeated: list[str] = []
    for n in (4, 5, 6):
        counts = Counter(tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1))
        for phrase, count in counts.items():
            joined = " ".join(phrase)
            if count > 1 and "debojit choudhury" not in joined:
                repeated.append(f"{count}x {joined}")
    return Check("markdown_repeated_4_to_6_word_phrases", not repeated, "none" if not repeated else "; ".join(repeated[:10]))


def markdown_checks(md: str, word_limit: int) -> list[Check]:
    checks: list[Check] = []
    checks.append(banned_metadata_check("markdown_no_diagnostics", md))
    wc = len(md.split())
    checks.append(Check("markdown_word_limit", wc <= word_limit, f"{wc}/{word_limit} words"))
    checks.append(Check("markdown_recent_professional_experience", "## Recent Professional Experience" in md, "required heading present"))
    checks.append(Check("markdown_no_old_professional_experience_heading", not re.search(r"^## Professional Experience\s*$", md, re.M), "old heading absent"))
    role_heading_hits = [line for line in md.splitlines() if ROLE_PREFIX_RE.search(line)]
    checks.append(Check("markdown_project_headings_no_role_prefix", not role_heading_hits, "none" if not role_heading_hits else "; ".join(role_heading_hits)))
    checks.append(duplicate_metrics_check(md))
    checks.append(repeated_phrases_check(md))
    return checks


def html_checks(html: str, md: str | None = None) -> list[Check]:
    visible = strip_html(html)
    checks: list[Check] = []
    checks.append(banned_metadata_check("html_no_diagnostics", html))
    remote_hits = []
    for name, pattern in {
        "script_tag": r"<\s*script\b",
        "link_tag": r"<\s*link\b",
        "css_import": r"@import",
        "css_url": r"url\s*\(",
        "http_url": r"https?://",
    }.items():
        if re.search(pattern, html, flags=re.I):
            remote_hits.append(name)
    # Allow candidate LinkedIn URL text but not as an asset. If the only http URL is visible LinkedIn text, do not count it as remote asset.
    if "http_url" in remote_hits:
        asset_html = re.sub(r">[^<]*https?://[^<]*<", "><", html)
        if not re.search(r"https?://", asset_html):
            remote_hits.remove("http_url")
    checks.append(Check("html_no_remote_assets_or_scripts", not remote_hits, "none" if not remote_hits else ", ".join(remote_hits)))
    checks.append(Check("html_technical_skills_label", "Technical Skills" in visible and "Technical Environment" not in visible, "Technical Skills present"))
    checks.append(Check("html_contact_panel", "Contact" in visible, "Contact present"))
    if md:
        md_metrics = extract_bold_metrics(md)
        missing = [m for m in md_metrics if m not in visible]
        checks.append(Check("html_preserves_markdown_metrics", not missing, "all metrics present" if not missing else "; ".join(missing[:10])))
    return checks


def main() -> None:
    parser = argparse.ArgumentParser(description="Review final resume artifacts.")
    parser.add_argument("--markdown", type=Path, help="Markdown resume path")
    parser.add_argument("--html", type=Path, help="HTML resume path")
    parser.add_argument("--word-limit", type=int, default=600)
    args = parser.parse_args()

    if not args.markdown and not args.html:
        parser.error("provide --markdown, --html, or both")

    md = read(args.markdown) if args.markdown else ""
    html = read(args.html) if args.html else ""

    checks: list[Check] = []
    if md:
        checks.extend(markdown_checks(md, args.word_limit))
    if html:
        checks.extend(html_checks(html, md if md else None))

    overall = all(c.passed for c in checks)
    print(f"overall={'PASS' if overall else 'FAIL'}")
    for check in checks:
        print(f"{check.name}={'PASS' if check.passed else 'FAIL'} - {check.detail}")
    sys.exit(0 if overall else 1)


if __name__ == "__main__":
    main()
