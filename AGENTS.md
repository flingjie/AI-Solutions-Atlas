# AGENTS.md

Conventions for AI coding agents working in this repository. Full detail is in
`CLAUDE.md` and the design spec under `docs/superpowers/specs/`.

## Core principles

- Evidence before conclusions. Every fact cites a source. No fabricated capabilities.
- Separate fact / inferred / assumption. Uncited claims are assumptions.
- Read-only: skills discover and analyze; they do not publish. Human approval is
  required before `status: published`.
- Markdown is the source of truth. There is no database and no web app.

## Commands

- Validate the repository: `python3 scripts/validate.py`

## Directory map

- `projects/` — project records (evidence base)
- `problems/` — problem analyses
- `solutions/` — solution patterns
- `research/` — research reports
- `templates/` — the four content templates
- `skills/` — AI workflow skills (shared with Claude Code via symlink)
- `domains/ai-marketing-gtm/` — the initial domain taxonomy
