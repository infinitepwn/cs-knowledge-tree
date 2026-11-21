#!/usr/bin/env python3
"""Sync course-repo Markdown notes into docs/notes/ for MkDocs.

Line-for-line port of scripts/sync-notes-to-docs.rb (kept for reference) with
additional subjects wired in. Output for the original four subjects is
byte-identical to the Ruby version.

Usage:
    python scripts/sync_notes_to_docs.py                 # all subjects
    python scripts/sync_notes_to_docs.py --out /tmp/out  # write elsewhere
    python scripts/sync_notes_to_docs.py --subjects operating-system
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
NOTES = DOCS / "notes"
SUBJECTS_DIR = ROOT / "subjects"

# Order matters: it drives the notes index and the MkDocs nav.
SUBJECTS = [
    {
        "slug": "computer-networking",
        "title": "计算机网络",
        "exclude": [r"\A\.claude/", r"\AAGENTS\.md\Z", r"\Aalice\.txt\Z"],
    },
    {
        "slug": "operating-system",
        "title": "操作系统",
        "exclude": [],
    },
    {
        "slug": "cryptography",
        "title": "密码学引论",
        "exclude": [
            r"\AUsers/",
            r"\Aexperiment/third_experiment/a2a_secure_flight_agent/",
            r"\Aexperiment/third_experiment/report/",
        ],
    },
    {
        "slug": "computer-systems",
        "title": "计算机系统原理",
        "exclude": [],
    },
    {
        "slug": "algorithm",
        "title": "算法设计与分析",
        "exclude": [r"(?:\A|/)README\.md\Z", r"(?:\A|/)index\.md\Z"],
    },
    {
        "slug": "cryptanalysis",
        "title": "密码分析学",
        "exclude": [
            r"(?:\A|/)README\.md\Z",
            r"(?:\A|/)index\.md\Z",
            r"\Aanimations/",
            r"\Alabs/",
        ],
    },
    {
        "slug": "machine-learning",
        "title": "机器学习",
        "exclude": [r"(?:\A|/)README\.md\Z", r"(?:\A|/)index\.md\Z"],
    },
    {
        "slug": "cybersecurity",
        "title": "网络安全",
        "exclude": [r"(?:\A|/)README\.md\Z", r"(?:\A|/)index\.md\Z"],
    },
    {
        "slug": "cybersecurity-lab",
        "title": "网络安全实验",
        "exclude": [
            r"(?:\A|/)README\.md\Z",
            r"(?:\A|/)index\.md\Z",
            r"(?:\A|/)TODO\.md\Z",
        ],
    },
    {
        "slug": "finite-field",
        "title": "有限域",
        "exclude": [r"(?:\A|/)README\.md\Z", r"(?:\A|/)index\.md\Z"],
    },
    {
        "slug": "rag",
        "title": "RAG",
        "exclude": [r"(?:\A|/)README\.md\Z", r"(?:\A|/)index\.md\Z"],
    },
]

# Never sync notes out of tooling/vault metadata directories.
GLOBAL_EXCLUDE = [
    r"\A\.obsidian/",
    r"\A\.vscode/",
    r"\A\.claude/",
    r"\A\.github/",
    r"\A__pycache__/",
    r"\Achroma_db/",
    r"\Anode_modules/",
    r"\Asite/",
]

OBSIDIAN_LINK = re.compile(r"\[\[([^\]|#]+)(#[^\]|]+)?(?:\|([^\]]+))?\]\]")
README_LINK = re.compile(r"\]\(([^)]+/)?README\.md(#[^)]+)?\)")
H1_LINE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
LEADING_H1 = re.compile(r"\A#\s+.+\n+")

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
ASSET_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".ico",
    ".pdf", ".mp4", ".mov", ".webm", ".zip", ".txt", ".csv", ".json",
    ".c", ".h", ".cpp", ".py", ".ipynb",
}


def read_text(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "gb18030"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def markdown_files(base: Path, excludes: list[str]) -> list[str]:
    patterns = [re.compile(p) for p in excludes]
    found: list[str] = []
    for path in base.rglob("*.md"):
        rel = path.relative_to(base).as_posix()
        if any(p.search(rel) for p in patterns):
            continue
        if rel in ("index.md", "README.md"):
            continue
        found.append(rel)
    return sorted(found)


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    lines = text.splitlines(keepends=True)
    close = None
    for index in range(1, len(lines)):
        if lines[index] in ("---\n", "---\r\n"):
            close = index
            break
    if close is None:
        return text
    return "".join(lines[close + 1 :])


def title_for(rel: str, text: str) -> str:
    match = H1_LINE.search(text)
    if match:
        return match.group(1).strip()
    return Path(rel).stem


def convert_obsidian_links(text: str, name_map: dict[str, str], current_dir: str) -> str:
    def replace_wiki(match: re.Match) -> str:
        target = match.group(1).strip()
        anchor = match.group(2) or ""
        label = match.group(3) or target
        dest = name_map.get(target)
        if not dest:
            return label
        return f"[{label}]({os.path.relpath(dest, current_dir).replace(os.sep, '/')}{anchor})"

    converted = OBSIDIAN_LINK.sub(replace_wiki, text)

    def replace_readme(match: re.Match) -> str:
        prefix = match.group(1) or ""
        anchor = match.group(2) or ""
        return f"]({prefix}index.md{anchor})"

    return README_LINK.sub(replace_readme, converted)


def strip_math_wrapper(formula: str) -> str:
    stripped = formula.strip()
    if stripped.startswith("\\(") and stripped.endswith("\\)"):
        return stripped[2:-2].strip()
    if stripped.startswith("\\[") and stripped.endswith("\\]"):
        return stripped[2:-2].strip()
    return stripped


def display_math_lines(prefix: str, formula: str) -> list[str]:
    body = strip_math_wrapper(formula)
    body_lines = body.splitlines(keepends=True)
    if not body.endswith("\n"):
        body_lines = [f"{body}\n"]
    spacer = "\n" if not prefix else f"{prefix.rstrip()}\n"
    return [
        spacer,
        f"{prefix}$$\n",
        *[f"{prefix}{line}" for line in body_lines],
        f"{prefix}$$\n",
        spacer,
    ]


INLINE_DOUBLE_DOLLAR = re.compile(r"(?<!\\)\$\$([^$\n]+?)\$\$")
INLINE_BRACKET = re.compile(r"\\\[(.+?)\\\]")
INLINE_SINGLE_DOLLAR = re.compile(r"(?<![\\$])\$([^$\n]+?)(?<![\\$])\$(?!\$)")

DISPLAY_SINGLE_LINE = re.compile(r"\A(\s*(?:>\s*)*)\$\$(.+?)\$\$\s*\Z")
BRACKET_SINGLE_LINE = re.compile(r"\A(\s*(?:>\s*)*)\\\[(.+?)\\\]\s*\Z")
DISPLAY_OPEN = re.compile(r"\A(\s*(?:>\s*)*)\$\$(.*?)\s*\Z")
BRACKET_OPEN = re.compile(r"\A(\s*(?:>\s*)*)\\\[(.*?)\s*\Z")
INLINE_SINGLE_LINE = re.compile(r"\A(\s*(?:>\s*)*)\$([^$].*[^$])\$\s*\Z")
DISPLAY_CLOSE = re.compile(r"\A\s*(?:>\s*)?(.*?)(?:\$\$|\\\])\s*\Z")


def normalize_math_blocks(text: str) -> str:
    in_fence = False
    in_display_math = False
    display_prefix = ""
    display_buffer: list[str] = []
    output: list[str] = []

    for line in text.splitlines(keepends=True):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence

        if in_display_math:
            match = None if in_fence else DISPLAY_CLOSE.match(line)
            if match:
                tail = match.group(1).strip()
                if tail:
                    display_buffer.append(f"{tail}\n")
                output.extend(display_math_lines(display_prefix, "".join(display_buffer)))
                in_display_math = False
                display_prefix = ""
                display_buffer = []
            else:
                display_buffer.append(line[len(display_prefix) :] if display_prefix and line.startswith(display_prefix) else line)
            continue

        match = None if in_fence else DISPLAY_SINGLE_LINE.match(line)
        if match:
            output.extend(display_math_lines(match.group(1), match.group(2)))
            continue

        match = None if in_fence else BRACKET_SINGLE_LINE.match(line)
        if match:
            output.extend(display_math_lines(match.group(1), match.group(2)))
            continue

        match = None if in_fence else DISPLAY_OPEN.match(line)
        if match:
            display_prefix = match.group(1)
            head = match.group(2).strip()
            if head:
                display_buffer.append(f"{head}\n")
            in_display_math = True
            continue

        match = None if in_fence else BRACKET_OPEN.match(line)
        if match:
            display_prefix = match.group(1)
            head = match.group(2).strip()
            if head:
                display_buffer.append(f"{head}\n")
            in_display_math = True
            continue

        match = None if in_fence else INLINE_SINGLE_LINE.match(line)
        if match:
            output.extend(display_math_lines(match.group(1), match.group(2)))
            continue

        converted = INLINE_DOUBLE_DOLLAR.sub(
            lambda m: f"\\({strip_math_wrapper(m.group(1))}\\)", line
        )
        converted = INLINE_BRACKET.sub(
            lambda m: f"\\({strip_math_wrapper(m.group(1))}\\)", converted
        )
        converted = INLINE_SINGLE_DOLLAR.sub(
            lambda m: f"\\({strip_math_wrapper(m.group(1))}\\)", converted
        )
        output.append(converted)

    if in_display_math:
        output.extend(display_math_lines(display_prefix, "".join(display_buffer)))

    return "".join(output)


def write_global_index(out_notes: Path, subjects: list[dict]) -> None:
    lines = [
        "# 课程笔记",
        "",
        "这里是课程仓库 Markdown 笔记的站内 Wiki 版本。笔记会同步到本站页面，可直接阅读、搜索和互相跳转。",
        "",
    ]
    for subject in subjects:
        lines.append(f"- [{subject['title']}]({subject['slug']}/index.md)")
    lines.append("")
    (out_notes / "index.md").write_text("\n".join(lines), encoding="utf-8", newline="")


def copy_referenced_assets(
    subject: dict, files: list[str], source: Path, dest_root: Path
) -> None:
    """Copy local files referenced from synced notes, mirroring repo layout.

    Only files that (a) exist inside the subject repo, (b) are not Markdown,
    and (c) look like a static asset are copied, so relative image/PDF links
    keep working on the published site. Everything else is left untouched.
    """
    copied = set()
    for rel in files:
        note = source / rel
        text = read_text(note)
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip().strip("<>").split("#")[0]
            if not target or target.startswith(("http://", "https://", "data:")):
                continue
            if target.lower().endswith(".md"):
                continue
            resolved = (note.parent / target).resolve()
            try:
                resolved.relative_to(source.resolve())
            except ValueError:
                continue
            if not resolved.is_file():
                continue
            if resolved.suffix.lower() not in ASSET_EXTENSIONS:
                continue
            repo_rel = resolved.relative_to(source.resolve())
            if repo_rel.as_posix() in copied:
                continue
            dest = dest_root / repo_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(resolved, dest)
            copied.add(repo_rel.as_posix())


def sync_subject(subject: dict, out_notes: Path, out_docs: Path) -> list[tuple[str, str, str]]:
    slug = subject["slug"]
    source = SUBJECTS_DIR / slug
    if not source.is_dir():
        print(f"skip {slug}: source {source} not found", file=sys.stderr)
        return []

    excludes = GLOBAL_EXCLUDE + subject["exclude"]
    dest_root = out_notes / slug
    files = markdown_files(source, excludes)
    copy_referenced_assets(subject, files, source, dest_root)

    name_map: dict[str, str] = {}
    for rel in files:
        name_map[Path(rel).stem] = (dest_root / rel).relative_to(out_docs).as_posix()

    entries: list[tuple[str, str, str]] = []
    for rel in files:
        source_file = source / rel
        dest_file = dest_root / rel
        dest_file.parent.mkdir(parents=True, exist_ok=True)

        raw = read_text(source_file)
        body = strip_frontmatter(raw).lstrip()
        title = title_for(rel, body)
        current_dir = dest_file.parent.relative_to(out_docs).as_posix()
        converted = normalize_math_blocks(convert_obsidian_links(body, name_map, current_dir))

        page = f"# {title}\n\n"
        page += f"> 来源：`{subject['title']} / {rel}`\n\n"
        page += LEADING_H1.sub("", converted, count=1)
        dest_file.write_text(page, encoding="utf-8", newline="")

        entries.append((rel, title, dest_file.relative_to(out_docs).as_posix()))

    groups: dict[str, list[tuple[str, str, str]]] = {}
    for entry in entries:
        dirname = os.path.dirname(entry[0])
        groups.setdefault(dirname if dirname else "入口", []).append(entry)

    lines = [f"# {subject['title']}笔记", "", "这里收录从课程仓库同步来的 Markdown 笔记，可在本站内直接阅读和搜索。", ""]
    for group, group_entries in groups.items():
        lines.append(f"## {group}")
        lines.append("")
        for _rel, title, dest in group_entries:
            rel_link = os.path.relpath(dest, f"notes/{slug}").replace(os.sep, "/")
            lines.append(f"- [{title}]({rel_link})")
        lines.append("")
    (dest_root / "index.md").write_text("\n".join(lines), encoding="utf-8", newline="")
    return entries


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None, help="output docs directory (default: docs/)")
    parser.add_argument("--subjects", default=None, help="comma separated subject slugs")
    args = parser.parse_args()

    subjects = SUBJECTS
    if args.subjects:
        wanted = {s.strip() for s in args.subjects.split(",") if s.strip()}
        subjects = [s for s in SUBJECTS if s["slug"] in wanted]

    out_docs = Path(args.out).resolve() if args.out else DOCS
    out_notes = out_docs / "notes"

    if out_notes.exists():
        shutil.rmtree(out_notes)
    out_notes.mkdir(parents=True, exist_ok=True)

    write_global_index(out_notes, subjects)

    print("Synced notes:")
    for subject in subjects:
        entries = sync_subject(subject, out_notes, out_docs)
        print(f"- {subject['slug']}: {len(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
