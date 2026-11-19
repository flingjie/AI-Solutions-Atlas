# CLAUDE.md

Guidance for Claude Code working in this repository.

## Project

AI Solutions Atlas is an evidence-based knowledge map of AI solutions for
marketing and go-to-market problems. Markdown files with YAML frontmatter are
the source of truth. No database, no web app, no runtime.

## Invariants

- Evidence before conclusions. Facts cite `sources[]` by index (`[1]`).
- Separate fact / inferred / assumption. Uncited claims must be `(assumption)`.
- No fabricated capabilities or market claims. Vendor claims are recorded as
  "official claim", never fact.
- Read-only by default. A record reaches `published` only after human approval.
- `validate.py` uses only the Python standard library.

## Commands

```bash
python3 scripts/validate.py   # validate all content records; exit 0 = clean
```

## Directory map

- `domains/<domain>/README.md` — domain definition and sub-category taxonomy
- `projects/` `problems/` `solutions/` `research/` — content records
- `templates/` — project / problem / solution / research templates
- `skills/` — five AI workflow skills; `_shared/` holds shared conventions
- `scripts/validate.py` — validation (structure, metadata, links, duplicates, evidence, references)

## Evidence model

A record's `sources` list holds `url`, `title`, `accessed`, `via` (`opencli` or
`webfetch`). In the body, `[1]` cites `sources[0]`. A conclusion derived from
cited evidence is `(inferred)`. An unverified statement is `(assumption)`.

## Skills

Use `skills/discover-projects`, `skills/analyze-problems`,
`skills/evaluate-solutions`, `skills/compare-projects`, and
`skills/content-review` for the corresponding workflows. Shared conventions are
in `skills/_shared/`.
