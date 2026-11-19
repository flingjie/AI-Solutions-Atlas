# AI Solutions Atlas

An evidence-based knowledge map of AI solutions, tools, implementation patterns,
and real business problems. The first domain is **AI Marketing & GTM**.

Every claim in this repository must trace to a cited source. Facts, inferred
conclusions, and unverified assumptions are kept separate. Vendor marketing
claims are recorded as claims, never as facts.

## Scope

- **In scope:** AI solutions for marketing and go-to-market problems, with an
  evidence trail to official or primary sources.
- **Out of scope:** opinion pieces without evidence, tool round-ups without a
  problem, unverifiable market-size claims, and general AI news.

## Structure

| Directory | Contents |
| --- | --- |
| `domains/` | Domain definitions and sub-category taxonomies |
| `projects/` | Project records (the evidence base) |
| `problems/` | Problem analyses |
| `solutions/` | Solution patterns |
| `research/` | Research reports and comparisons |
| `templates/` | Reusable Markdown templates |
| `skills/` | AI workflow skills (symlinked to `.claude/skills` and `.codex/skills`) |
| `scripts/` | Validation script |

## Working with this repository

### For humans

Read `CONTRIBUTING.md` to add or review content. Records follow one of the four
templates in `templates/`. Every record carries YAML frontmatter with a stable
`id` and a `sources` list.

### For AI agents

Read `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex). Use the five skills in
`skills/` to discover, analyze, evaluate, compare, and review content. Run
`python3 scripts/validate.py` after any edit.

## Principles

1. Evidence before conclusions.
2. Quality over quantity.
3. Problems before tools.
4. Separate facts, inferences, and assumptions.
5. No fabricated capabilities or market claims.
6. Consistent content structure.
7. Human approval before publishing.
8. Avoid premature technical complexity.

## Status

See `ROADMAP.md`.
