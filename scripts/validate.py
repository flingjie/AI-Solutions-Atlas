#!/usr/bin/env python3
"""Validate Atlas content records. Stdlib only. Exit 1 on errors, 0 otherwise."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIRS = ("projects", "problems", "solutions", "research")
TYPES = {"project", "problem", "solution", "research"}
STATUSES = {"draft", "review", "published"}
BASE_REQUIRED = ("id", "title", "type", "domain", "status", "created", "updated")
TYPE_REQUIRED = {
    "project": ("company", "category", "url"),
    "problem": ("who", "pain_points"),
    "solution": ("solves", "mechanism"),
    "research": ("question", "findings"),
}
ID_RE = re.compile(r"^[a-z0-9-]+$")
LIST_RE = re.compile(r"^\[(.*)\]$")


def _scalar(raw: str):
    raw = raw.strip().strip('"').strip("'")
    if raw in ("[]", ""):
        return []
    m = LIST_RE.match(raw)
    if m:
        return [x.strip().strip('"') for x in m.group(1).split(",") if x.strip()]
    if raw in ("true", "True"):
        return True
    if raw in ("false", "False"):
        return False
    try:
        return int(raw)
    except ValueError:
        return raw


def _parse_sources(lines, i):
    items = []
    cur = None
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        stripped = line.lstrip()
        if stripped.startswith("- "):
            cur = {}
            items.append(cur)
            key, _, val = stripped[2:].partition(":")
            cur[key.strip()] = _scalar(val)
        elif line.startswith("  ") and cur is not None:
            key, _, val = stripped.partition(":")
            cur[key.strip()] = _scalar(val)
        else:
            break
        i += 1
    return items, i


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    data = {}
    lines = block.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if key == "sources" and rest == "":
            data[key], i = _parse_sources(lines, i + 1)
        else:
            data[key] = _scalar(rest)
            i += 1
    return data


def _collect(root: Path):
    for d in CONTENT_DIRS:
        dpath = root / d
        if not dpath.is_dir():
            continue
        for f in sorted(dpath.glob("*.md")):
            yield d, f


def validate(root: Path):
    """Return a list of (severity, message) tuples. severity is error or warning."""
    out = []
    seen_ids = {}
    for d, f in _collect(root):
        text = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            out.append(("error", f"{f}: missing or malformed frontmatter"))
            continue
        rid = fm.get("id")
        if not rid or not ID_RE.match(str(rid)):
            out.append(("error", f"{f}: id missing or not kebab-case"))
            continue
        if rid in seen_ids:
            out.append(("error", f"{f}: duplicate id {rid} (also {seen_ids[rid]})"))
        seen_ids[rid] = f
        for k in BASE_REQUIRED:
            if k not in fm:
                out.append(("error", f"{f}: missing required field {k}"))
        if not fm.get("title"):
            out.append(("error", f"{f}: title is empty"))
        typ = fm.get("type")
        if typ not in TYPES:
            out.append(("error", f"{f}: invalid type {typ!r}"))
            continue
        if fm.get("status") not in STATUSES:
            out.append(("error", f"{f}: invalid status {fm.get('status')!r}"))
        for k in TYPE_REQUIRED.get(typ, ()):
            if k not in fm:
                out.append(("error", f"{f}: missing {typ} field {k}"))
        if "sources" not in fm:
            out.append(("error", f"{f}: missing sources"))
        elif not fm.get("sources"):
            if fm.get("status") == "published":
                out.append(("error", f"{f}: published with no sources"))
            else:
                out.append(("warning", f"{f}: empty sources"))
        for ref_k in ("solves", "used_by"):
            refs = fm.get(ref_k) or []
            if isinstance(refs, str):
                refs = [refs]
            for ref in refs:
                if ref and not any((root / d / f"{ref}.md").exists() for d in CONTENT_DIRS):
                    out.append(("error", f"{f}: {ref_k} references missing id {ref}"))
    return out


def main(argv=None):
    out = validate(ROOT)
    for severity, message in out:
        print(f"{severity}: {message}")
    if any(severity == "error" for severity, _ in out):
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
