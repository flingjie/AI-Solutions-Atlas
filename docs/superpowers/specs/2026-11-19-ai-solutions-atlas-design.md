# AI Solutions Atlas — Design Spec

Date: 2026-11-19
Status: approved

## 1. Objective

AI Solutions Atlas is an open-source, evidence-based knowledge map of AI solutions,
tools, implementation patterns, and real business problems. The first research domain
is AI Marketing & GTM. Later domains are added based on validated needs.

## 2. Core Principles

1. Evidence before conclusions.
2. Quality over quantity.
3. Problems before tools.
4. Separate facts, observations (inferred), and opinions (assumptions).
5. No fabricated project capabilities or market claims.
6. Consistent content structure.
7. Human approval before publishing.
8. Avoid premature technical complexity.

## 3. Key Decisions

- **Location and repository.** New git repo at `/Users/lingjiefan/underway/AI-Solutions-Atlas`,
  default branch `main`.
- **Language.** All content, templates, and validation scripts are in English.
- **Approach.** Convention-first: Markdown is the single source of truth. No runtime,
  no database, no web app. Validation is one lightweight Python script (`scripts/validate.py`)
  run after edits.
- **Skills form.** Five skills written as Claude Code skills (`SKILL.md` with YAML
  frontmatter). They are symlinked into both `.claude/skills` and `.codex/skills` so
  Claude Code and Codex share one source of truth under `skills/`.
- **Evidence capture tool.** `opencli` is the preferred tool for capturing evidence from
  official pages. `WebFetch` is the fallback for sites without an opencli adapter or for
  contributors without opencli. Each source records the capture method in `via`.

## 4. Repository Structure

```
AI-Solutions-Atlas/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── ROADMAP.md
├── .gitignore
├── .claude/skills -> ../skills        # symlink (Claude Code)
├── .codex/skills   -> ../skills        # symlink (Codex)
├── skills/
│   ├── discover-projects/{SKILL.md, references/}
│   ├── analyze-problems/{SKILL.md, references/}
│   ├── evaluate-solutions/{SKILL.md, references/}
│   ├── compare-projects/{SKILL.md, references/}
│   ├── content-review/{SKILL.md, references/}
│   └── _shared/                        # shared conventions: evidence model, frontmatter spec
├── domains/
│   └── ai-marketing-gtm/README.md      # domain definition, sub-categories, boundaries
├── problems/                           # problem analysis records
├── solutions/                          # solution pattern records
├── projects/                           # project records (evidence base)
├── research/                           # research reports and comparisons
├── templates/                          # reusable Markdown templates (4 types)
├── scripts/validate.py                 # lightweight validation (stdlib only)
└── docs/superpowers/specs/             # design and plan documents
```

The `skills/` directory is the single source of truth for skills. The symlinks use a
relative target (`../skills`) so the repository stays portable.

## 5. Evidence Model

Every content record has a YAML frontmatter:

```yaml
---
id: project-openai-customer-os
title: OpenAI — customer OS
type: project                        # project | problem | solution | research
domain: ai-marketing-gtm
status: draft                        # draft | review | published
created: 2026-11-19
updated: 2026-11-19
sources:
  - url: https://openai.com/blog/xxx
    title: "Introducing ..."
    accessed: 2026-11-19
    via: opencli                       # opencli | webfetch
---
```

The body separates three layers:

- **Fact** — a claim with an inline citation `[1]` that points to `sources[0]` and comes
  from an official source.
- **Inferred** — a conclusion derived from cited evidence, marked `(inferred)`.
- **Assumption** — an unverified statement, marked `(assumption)` and explicitly noted
  as unverified.

Vendor market claims (for example "300% growth", "industry-leading") are recorded only as
"official claim", never as fact.

## 6. Content Types and Templates

`projects/` is the evidence base. Other types cite it; they do not copy it.

| Type | Directory | Question it answers | Type-specific fields |
| --- | --- | --- | --- |
| Project record | `projects/` | What is this product/tool, who made it, what do they claim | `company` `category` `url` `claims` |
| Problem analysis | `problems/` | Who has this problem, what is the pain, how is it handled today | `who` `current_approach` `pain_points` |
| Solution pattern | `solutions/` | How is this problem solved, what is the mechanism, what are the limits | `solves` `used_by` `mechanism` `limitations` |
| Research report | `research/` | A multi-source synthesis of one research question | `question` `method` `findings` `conclusions` |

Each `domains/<domain>/README.md` defines the sub-category taxonomy. A project `category`
must be in that taxonomy. Templates live in `templates/`, one per type.

## 7. Skills

Each skill has Purpose, Input, Output, Workflow, Evidence requirements, Quality checks,
and an Example. They use file operations (Read/Write/Edit + grep + `scripts/validate.py`).
Shared conventions live in `skills/_shared/`.

| Skill | Purpose | Output | Evidence bar |
| --- | --- | --- | --- |
| `discover-projects` | Find real projects from official sources | `projects/*.md` | Each claim has an official URL; no fabricated capability; status `draft` |
| `analyze-problems` | Derive real problems from projects/discussions | `problems/*.md` | Pain has evidence; fact/inferred/assumption separated; cites projects |
| `evaluate-solutions` | Assess solution patterns | `solutions/*.md` | Mechanism is supported; limitations are explicit; cites problems+projects |
| `compare-projects` | Compare 2+ projects on one axis | `research/*.md` | No invented numbers; same-axis comparable; each cell cited or "unknown" |
| `content-review` | Review against the 8 principles + structure + evidence | review findings + fixes | Run `validate.py`; check each citation against its source |

## 8. Validation

`scripts/validate.py` uses only the Python standard library. It reports errors and
warnings and exits non-zero on errors. It checks:

1. Frontmatter structure (required fields, valid `type`/`status`/`category`).
2. Metadata (`id` unique, `title` non-empty).
3. Broken links (internal references resolve to existing files).
4. Duplicate records (same `id`, or same `title` + `company`).
5. Missing evidence (`sources` empty -> warning; `status=published` with no sources -> error).
6. Invalid internal references (`solves`/`used_by`/`related` point to a missing id).

## 9. Sample Content

Create a small, real sample set under AI Marketing & GTM: 2 project records, 1 problem
analysis, 1 solution pattern. Use real projects and official sources. Gather evidence
with `opencli` (fallback `WebFetch`). Mark anything unverified as `(assumption)`.

## 10. Phases

1. **Foundation** — README, AGENTS.md, CLAUDE.md, CONTRIBUTING, GOVERNANCE, ROADMAP,
   plus positioning, scope/boundaries, domain taxonomy, content guidelines, evaluation
   criteria, maintenance policy.
2. **Content architecture** — the `domains/problems/solutions/projects/research/templates/skills`
   directories and the four Markdown templates.
3. **AI workflow** — the five skills.
4. **Validation** — `scripts/validate.py`.
5. **Initial content** — the small sample set, then a consistency review with a list of
   remaining gaps.

## 11. Constraints

- Keep version one simple.
- No database, no web app, no autonomous crawling, no unnecessary abstractions.
- Do not invent information to fill templates.
- Markdown is the initial source of truth.
