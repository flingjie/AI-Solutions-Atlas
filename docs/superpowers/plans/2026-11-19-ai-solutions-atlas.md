# AI Solutions Atlas Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Initialize the AI Solutions Atlas — an open-source, Markdown-only, evidence-based knowledge map of AI solutions, with documentation, templates, five skills, a validation script, and a small real sample set.

**Architecture:** Markdown files with YAML frontmatter are the single source of truth. Five skills (under `skills/`, symlinked into `.claude/skills` and `.codex/skills`) guide AI agents. One stdlib-only Python script (`scripts/validate.py`) checks structure, metadata, links, duplicates, evidence, and internal references after edits.

**Tech Stack:** Markdown, YAML frontmatter, Python 3 standard library only (no third-party deps), `git`, `opencli` (evidence capture) with `WebFetch` fallback.

## Global Constraints

- All content, templates, and scripts are in **English**.
- No database, no web app, no autonomous crawling, no Python package beyond a single stdlib script.
- Markdown is the initial source of truth.
- `validate.py` uses **only the Python standard library** (no PyYAML, no requests).
- Skills are Claude Code `SKILL.md` format: YAML frontmatter with `name` + `description`, then instructions.
- Evidence rule: facts cite `sources[]` by index (`[1]`); inferred claims are marked `(inferred)`; unverified claims are marked `(assumption)` and stated as unverified. Vendor claims are "official claim", never fact.
- Statuses: `draft`, `review`, `published`. Only `published` requires a human approval.
- Record types: `project`, `problem`, `solution`, `research`.
- IDs and domains are lowercase kebab-case (`^[a-z0-9-]+$`).

---

## File Structure

```
AI-Solutions-Atlas/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── ROADMAP.md
├── .gitignore
├── .claude/skills -> ../skills
├── .codex/skills -> ../skills
├── domains/ai-marketing-gtm/README.md
├── problems/
├── solutions/
├── projects/
├── research/
├── templates/{project.md, problem.md, solution.md, research.md}
├── skills/
│   ├── _shared/{evidence-model.md, frontmatter.md}
│   ├── discover-projects/{SKILL.md, references/}
│   ├── analyze-problems/{SKILL.md, references/}
│   ├── evaluate-solutions/{SKILL.md, references/}
│   ├── compare-projects/{SKILL.md, references/}
│   └── content-review/{SKILL.md, references/}
├── scripts/validate.py
└── tests/test_validate.py
```

Each content record lives in `projects/`, `problems/`, `solutions/`, or `research/`, one file per record, named `<id>.md`.

---

### Task 1: Repository scaffolding

**Files:**
- Create: `.gitignore`
- Create: `.claude/skills` (symlink), `.codex/skills` (symlink)
- Create: empty `problems/`, `solutions/`, `projects/`, `research/` dirs (with `.gitkeep`)

**Interfaces:**
- Produces: the directory tree every later task writes into.

- [ ] **Step 1: Write `.gitignore`**

```bash
cat > .gitignore <<'EOF'
.DS_Store
__pycache__/
*.pyc
.venv/
EOF
```

- [ ] **Step 2: Create content directories**

```bash
mkdir -p problems solutions projects research domains/ai-marketing-gtm templates skills/_shared
touch problems/.gitkeep solutions/.gitkeep projects/.gitkeep research/.gitkeep
```

- [ ] **Step 3: Create skill symlinks (relative, portable)**

```bash
mkdir -p .claude .codex
ln -sfn ../skills .claude/skills
ln -sfn ../skills .codex/skills
ls -la .claude/skills .codex/skills
```

Expected: both resolve to `skills/`.

- [ ] **Step 4: Commit**

```bash
git add .gitignore .claude/skills .codex/skills problems solutions projects research domains templates skills
git commit -m "chore: scaffold repository directories and skill symlinks"
```

---

### Task 2: README.md

**Files:**
- Create: `README.md`

**Interfaces:**
- Produces: project positioning, scope, and navigation referenced by CONTRIBUTING/GOVERNANCE.

- [ ] **Step 1: Write `README.md`**

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README"
```

---

### Task 3: AGENTS.md and CLAUDE.md

**Files:**
- Create: `AGENTS.md`
- Create: `CLAUDE.md`

**Interfaces:**
- Produces: the two agent instruction files that point agents at `scripts/validate.py` and `skills/`.

- [ ] **Step 1: Write `AGENTS.md`**

```markdown
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
```

- [ ] **Step 2: Write `CLAUDE.md`**

```markdown
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
```

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md CLAUDE.md
git commit -m "docs: add agent instruction files"
```

---

### Task 4: CONTRIBUTING, GOVERNANCE, ROADMAP

**Files:**
- Create: `CONTRIBUTING.md`
- Create: `GOVERNANCE.md`
- Create: `ROADMAP.md`

**Interfaces:**
- Produces: contribution guidelines, evaluation criteria, maintenance policy, and roadmap referenced by README.

- [ ] **Step 1: Write `CONTRIBUTING.md`**

```markdown
# Contributing

Contributions are content records, templates, skills, or validation
improvements. Follow the evidence rules.

## Content guidelines

1. Start from a problem, not a tool.
2. Use one of the four templates in `templates/`.
3. Give every record a stable kebab-case `id`.
4. Put every fact's source in `sources[]` and cite it in the body with `[n]`.
5. Mark inferred conclusions `(inferred)` and unverified claims `(assumption)`.
6. Record vendor marketing claims as "official claim", never as fact.
7. Do not invent numbers, capabilities, or sources to fill a template.

## Workflow

1. `discover-projects` to find a real project.
2. `analyze-problems` to derive the problem it addresses.
3. `evaluate-solutions` to assess the solution pattern.
4. `content-review` to check structure, evidence, and references.
5. Run `python3 scripts/validate.py`. Fix all errors.
6. Submit for human review. A record becomes `published` only after approval.

## Evidence capture

Prefer `opencli` for capturing official pages. Use `WebFetch` when opencli has
no adapter for the site or you do not have opencli installed. Record the method
in each source's `via` field.
```

- [ ] **Step 2: Write `GOVERNANCE.md`**

```markdown
# Governance

## Roles

- **Contributor** — adds or edits content; must pass `validate.py`.
- **Reviewer** — approves content for `published`; checks evidence quality.
- **Maintainer** — sets scope, taxonomy, and merge policy.

## Evaluation criteria

A record is accepted when:

1. Its `id` is stable and unique.
2. It follows its template and passes `validate.py`.
3. Every fact traces to a source in `sources[]`.
4. Inferred and assumed claims are clearly marked.
5. It records no fabricated capability or market claim.

## Publishing

- New records start as `draft`.
- A reviewer may move a record to `review`.
- A `published` record requires an explicit human approval. There is no
  automatic publishing.

## Maintenance policy

- Stale records (source URL dead, claim outdated) are flagged, not silently edited.
- A record whose sources no longer resolve is moved back to `draft`.
- Domain taxonomy changes require a maintainer decision and a migration note.

## Decision making

- Changes to templates, the evidence model, or `validate.py` require maintainer
  review because they affect every record.
```

- [ ] **Step 3: Write `ROADMAP.md`**

```markdown
# Roadmap

## Phase 1 — Foundation (current)

Repository scaffolding, documentation, positioning, scope, governance, roadmap.

## Phase 2 — Content architecture

Directories and four reusable templates.

## Phase 3 — AI workflow

Five skills: discover-projects, analyze-problems, evaluate-solutions,
compare-projects, content-review.

## Phase 4 — Validation

`scripts/validate.py` with six checks.

## Phase 5 — Initial content

A small real sample set and a consistency review with a gaps list.

## Later (not planned)

- More domains beyond AI Marketing & GTM, based on validated need.
- A thin CLI over `validate.py` if the convention-first approach shows stress.
- Comparison-report template if `compare-projects` output outgrows `research/`.
```

- [ ] **Step 4: Commit**

```bash
git add CONTRIBUTING.md GOVERNANCE.md ROADMAP.md
git commit -m "docs: add contributing, governance, and roadmap"
```

---

### Task 5: Domain taxonomy

**Files:**
- Create: `domains/ai-marketing-gtm/README.md`

**Interfaces:**
- Produces: the `category` values that project records must use.

- [ ] **Step 1: Write `domains/ai-marketing-gtm/README.md`**

```markdown
# Domain: AI Marketing & GTM

AI solutions for marketing and go-to-market problems.

## Definition

A solution is in scope when it applies machine learning or a large language
model to a marketing or go-to-market task, and its existence can be traced to
an official or primary source.

## Sub-categories

A project record's `category` must be one of:

- `content-generation` — copy, creative, and asset generation
- `personalization` — segmentation, targeting, and individualized messaging
- `analytics` — attribution, forecasting, and campaign measurement
- `workflow` — orchestration, routing, and agentic marketing operations
- `gtm-research` — lead, account, and market research for go-to-market

## Boundaries

- **In:** products with an official page and a stated marketing/GTM use case.
- **Out:** horizontal models with no marketing-specific product, pure
  consulting services, and tools with no public evidence.
```

- [ ] **Step 2: Commit**

```bash
git add domains/ai-marketing-gtm/README.md
git commit -m "docs: add ai-marketing-gtm domain taxonomy"
```

---

### Task 6: Four content templates

**Files:**
- Create: `templates/project.md`, `templates/problem.md`, `templates/solution.md`, `templates/research.md`

**Interfaces:**
- Produces: the frontmatter schema and body structure every record must follow. `validate.py` (Task 13) enforces these fields.

- [ ] **Step 1: Write `templates/project.md`**

```markdown
---
id: project-<name>
title: <Product name>
type: project
domain: ai-marketing-gtm
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
company: <Company name>
category: <content-generation|personalization|analytics|workflow|gtm-research>
url: <official URL>
claims: []
sources: []
---

# <Product name>

## What it is

One or two sentences. Cite the official page.

## Official claims

A bullet list of claims the vendor makes, each cited `[n]` and recorded as an
"official claim" (not a fact).

## Evidence

### Facts

- Cited statements from `sources[]`.

### Inferred

- `(inferred)` conclusions derived from the facts.

### Assumptions

- `(assumption)` statements, explicitly unverified.
```

- [ ] **Step 2: Write `templates/problem.md`**

```markdown
---
id: problem-<name>
title: <Problem statement>
type: problem
domain: ai-marketing-gtm
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
who: <who has this problem>
current_approach: <how they handle it today>
pain_points: []
sources: []
---

# <Problem statement>

## Who

The people or teams with this problem, with evidence.

## Pain points

Bullet list, each cited or marked `(assumption)`.

## Current approach

How it is handled without the AI solution, with evidence where available.
```

- [ ] **Step 3: Write `templates/solution.md`**

```markdown
---
id: solution-<name>
title: <Solution pattern name>
type: solution
domain: ai-marketing-gtm
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
solves: [problem-<id>]
used_by: [project-<id>]
mechanism: <one-sentence mechanism>
limitations: []
sources: []
---

# <Solution pattern name>

## Mechanism

How the solution works, with cited evidence.

## Who uses it

Project records this pattern appears in (`used_by`).

## Limitations

Bullet list, each cited or marked `(assumption)`.
```

- [ ] **Step 4: Write `templates/research.md`**

```markdown
---
id: research-<name>
title: <Research question>
type: research
domain: ai-marketing-gtm
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
question: <the question>
method: <how the research was done>
findings: []
conclusions: []
sources: []
---

# <Research question>

## Method

How the research was conducted.

## Findings

Bullet list with cited evidence.

## Conclusions

What follows from the findings, marked `(inferred)` where applicable.
```

- [ ] **Step 5: Commit**

```bash
git add templates/
git commit -m "docs: add four content templates"
```

---

### Task 7: Shared skill conventions

**Files:**
- Create: `skills/_shared/evidence-model.md`, `skills/_shared/frontmatter.md`

**Interfaces:**
- Produces: the evidence rules and frontmatter spec that every skill's `references/` links to.

- [ ] **Step 1: Write `skills/_shared/evidence-model.md`**

```markdown
# Evidence model

## Three layers

- **Fact** — a statement with an inline citation `[n]` that points to
  `sources[n-1]` (1-indexed) and comes from an official or primary source.
- **Inferred** — a conclusion derived from cited facts, marked `(inferred)`.
- **Assumption** — an unverified statement, marked `(assumption)` and stated as
  unverified.

## Rules

1. A fact without a citation is an assumption.
2. A vendor marketing claim ("300% growth", "industry-leading") is recorded as
   an "official claim", never as a fact.
3. Never invent a number, capability, or source to complete a record.
4. Prefer `opencli` to capture an official page; use `WebFetch` as fallback.
   Record the method in the source's `via` field.
```

- [ ] **Step 2: Write `skills/_shared/frontmatter.md`**

```markdown
# Frontmatter spec

Every record has a YAML frontmatter block between `---` lines.

## Base fields (all types)

- `id` — stable kebab-case slug, e.g. `project-<name>`
- `title` — human-readable title
- `type` — `project` | `problem` | `solution` | `research`
- `domain` — e.g. `ai-marketing-gtm`
- `status` — `draft` | `review` | `published`
- `created` / `updated` — `YYYY-MM-DD`
- `sources` — list; each item has `url`, `title`, `accessed`, `via`

## Type fields

- `project`: `company`, `category`, `url`, `claims`
- `problem`: `who`, `current_approach`, `pain_points`
- `solution`: `solves`, `used_by`, `mechanism`, `limitations`
- `research`: `question`, `method`, `findings`, `conclusions`

`solves`, `used_by`, and any cross-reference must point to existing record ids.
```

- [ ] **Step 3: Commit**

```bash
git add skills/_shared/
git commit -m "docs: add shared skill conventions"
```

---

### Task 8: discover-projects skill

**Files:**
- Create: `skills/discover-projects/SKILL.md`

**Interfaces:**
- Consumes: `skills/_shared/evidence-model.md`, `skills/_shared/frontmatter.md`, `templates/project.md`, `domains/ai-marketing-gtm/README.md`
- Produces: a workflow that writes `projects/<id>.md` records.

- [ ] **Step 1: Write `skills/discover-projects/SKILL.md`**

````markdown
---
name: discover-projects
description: >
  Find a real AI solution for marketing/GTM from an official source and create
  a `projects/` record. Use when asked to "find a new AI marketing tool",
  "add a project", or "research a vendor". Captures evidence with opencli
  (WebFetch fallback); writes no fabricated capability and leaves status draft.
---

# discover-projects

Create one `projects/<id>.md` record per project. The record is evidence-only:
official claims are recorded as claims, never as facts.

## Input

- A project name, a URL, or a search topic in the AI Marketing & GTM domain.

## Output

- A new `projects/<id>.md` following `templates/project.md`.

## Workflow

1. Resolve the project's official page (the vendor site or a primary source).
2. Capture the page with `opencli`; use `WebFetch` if opencli has no adapter.
   Record `url`, `title`, `accessed`, and `via`.
3. Pick a `category` from `domains/ai-marketing-gtm/README.md`.
4. Fill the template using only what the source states. Do not infer a
   capability the source does not state.
5. Put every cited claim's URL in `sources[]` and cite it in the body `[n]`.
6. Mark anything unverified as `(assumption)`.
7. Leave `status: draft`.

## Evidence requirements

- At least one `sources[]` entry with an official URL.
- No fabricated capability or market claim.

## Quality checks

- `id` is unique and kebab-case.
- `category` is in the domain taxonomy.
- Every body fact has a `[n]` citation.
- Run `python3 scripts/validate.py`; fix all errors.

## Example

Input: "Find the project behind OpenAI's customer OS blog post."

Output: `projects/project-openai-customer-os.md` with `company: OpenAI`,
`category: workflow`, `url` pointing to the blog post, `claims` listing the
vendor's stated claims, and body facts cited `[1]`.
````

- [ ] **Step 2: Commit**

```bash
git add skills/discover-projects/
git commit -m "feat: add discover-projects skill"
```

---

### Task 9: analyze-problems skill

**Files:**
- Create: `skills/analyze-problems/SKILL.md`

**Interfaces:**
- Consumes: shared conventions, `templates/problem.md`, `projects/`
- Produces: `problems/<id>.md` records.

- [ ] **Step 1: Write `skills/analyze-problems/SKILL.md`**

````markdown
---
name: analyze-problems
description: >
  Derive a real marketing/GTM problem from projects and discussions and create
  a `problems/` record. Use when asked to "find the problem this tool solves"
  or "analyze a pain point". Keeps fact/inferred/assumption separate and cites
  project records.
---

# analyze-problems

Create one `problems/<id>.md` per problem. The problem must trace to evidence,
not be invented to match a tool.

## Input

- One or more `projects/` records, or external discussions (issues, forums).

## Output

- A new `problems/<id>.md` following `templates/problem.md`.

## Workflow

1. Identify who has the problem and how they handle it today.
2. Collect evidence: project records, official docs, or primary discussions.
3. Fill the template. Separate facts (cited), `(inferred)` conclusions, and
   `(assumption)` statements.
4. Set `who` and `pain_points`. Cite `projects/` ids where relevant.
5. Leave `status: draft`.

## Evidence requirements

- Each pain point is cited or marked `(assumption)`.
- No invented user complaint.

## Quality checks

- `who` is specific (a role, not "everyone").
- `pain_points` is non-empty.
- Cross-references resolve to existing `projects/` ids.
- Run `python3 scripts/validate.py`.

## Example

Input: the project record for an AI copywriting tool.

Output: `problems/problem-slow-copy-production.md` with `who: marketing teams`,
`current_approach: manual writing and editing`, and pain points cited from the
project record.
````

- [ ] **Step 2: Commit**

```bash
git add skills/analyze-problems/
git commit -m "feat: add analyze-problems skill"
```

---

### Task 10: evaluate-solutions skill

**Files:**
- Create: `skills/evaluate-solutions/SKILL.md`

**Interfaces:**
- Consumes: shared conventions, `templates/solution.md`, `problems/`, `projects/`
- Produces: `solutions/<id>.md` records.

- [ ] **Step 1: Write `skills/evaluate-solutions/SKILL.md`**

````markdown
---
name: evaluate-solutions
description: >
  Assess a solution pattern for a marketing/GTM problem and create a
  `solutions/` record. Use when asked to "explain how this problem is solved"
  or "evaluate a solution approach". Mechanism must be cited; limitations are
  explicit.
---

# evaluate-solutions

Create one `solutions/<id>.md` per pattern. A solution record links a problem
(`solves`) to the projects that use it (`used_by`).

## Input

- A problem id and one or more project ids.

## Output

- A new `solutions/<id>.md` following `templates/solution.md`.

## Workflow

1. Read the `problems/` and `projects/` records.
2. Write the `mechanism` in one sentence, citing the source that describes it.
3. List `used_by` project ids and `solves` problem ids.
4. Write `limitations`, each cited or marked `(assumption)`.
5. Leave `status: draft`.

## Evidence requirements

- `mechanism` is supported by a source, not invented.
- `limitations` is honest; an empty list is an error.

## Quality checks

- `solves` and `used_by` resolve to existing record ids.
- No invented numbers or capabilities.
- Run `python3 scripts/validate.py`.

## Example

Input: `problem-slow-copy-production` + the AI copywriting project record.

Output: `solutions/solution-llm-draft-then-edit.md` with `mechanism` describing
LLM first-draft generation plus human editing, cited, and `limitations` noting
factuality risk.
````

- [ ] **Step 2: Commit**

```bash
git add skills/evaluate-solutions/
git commit -m "feat: add evaluate-solutions skill"
```

---

### Task 11: compare-projects skill

**Files:**
- Create: `skills/compare-projects/SKILL.md`

**Interfaces:**
- Consumes: shared conventions, `templates/research.md`, `projects/`
- Produces: `research/<id>.md` comparison reports.

- [ ] **Step 1: Write `skills/compare-projects/SKILL.md`**

````markdown
---
name: compare-projects
description: >
  Compare two or more projects on one axis and write a `research/` report. Use
  when asked to "compare X and Y" or "which tool is better for Z". No invented
  numbers; each cell is cited or marked unknown.
---

# compare-projects

Write one `research/<id>.md` comparison. Comparison is same-axis and evidence
based; it does not assign a combined score.

## Input

- Two or more `projects/` ids and one comparison axis.

## Output

- A new `research/<id>.md` following `templates/research.md`.

## Workflow

1. Read each project record.
2. Choose a single comparison axis (for example "copy quality", "workflow fit").
3. Fill `findings` as a same-axis comparison. Cite each cell or write "unknown".
4. Write `conclusions`, marked `(inferred)` where derived.
5. Leave `status: draft`.

## Evidence requirements

- Each comparison cell is cited or explicitly "unknown".
- No invented metric or score.

## Quality checks

- A single comparison axis, not a feature dump.
- Cross-references resolve.
- Run `python3 scripts/validate.py`.

## Example

Input: two copywriting project ids, axis "human editing overhead".

Output: `research/research-copy-editing-overhead.md` comparing the two, each
cell cited from the project records.
````

- [ ] **Step 2: Commit**

```bash
git add skills/compare-projects/
git commit -m "feat: add compare-projects skill"
```

---

### Task 12: content-review skill

**Files:**
- Create: `skills/content-review/SKILL.md`

**Interfaces:**
- Consumes: shared conventions, `scripts/validate.py`
- Produces: review findings and fixes on any content record.

- [ ] **Step 1: Write `skills/content-review/SKILL.md`**

````markdown
---
name: content-review
description: >
  Review Atlas content against the eight principles, structure, and evidence
  rules, and fix findings. Use when asked to "review this record" or "check the
  repository for quality". Runs scripts/validate.py and checks each citation.
---

# content-review

Review records for correctness, evidence, and structure. Never fabricate a fix.

## Input

- A record path, a directory, or the whole repository.

## Output

- A list of findings and the applied fixes.

## Workflow

1. Run `python3 scripts/validate.py` and fix every error.
2. For each record, check the eight principles in order.
3. Check every `[n]` citation resolves to `sources[n-1]`.
4. Check facts are cited, inferences are `(inferred)`, and assumptions are
   `(assumption)`.
5. Check vendor claims are recorded as claims, not facts.
6. Fix or flag; do not invent evidence to resolve a gap.

## Evidence requirements

- A finding must point to the exact record and field.

## Quality checks

- `python3 scripts/validate.py` exits 0 after fixes.
- No finding left unresolved without a flag.

## Example

Input: a project record missing `sources`.

Output: a finding "missing evidence" and the fix adding the official URL with
`via` set, or a flag if no source exists.
````

- [ ] **Step 2: Commit**

```bash
git add skills/content-review/
git commit -m "feat: add content-review skill"
```

---

### Task 13: Validation script (TDD)

**Files:**
- Create: `scripts/validate.py`
- Create: `tests/test_validate.py`

**Interfaces:**
- Produces: `validate()` returns `list[tuple[severity, message]]` where severity is
  `"error"` or `"warning"`. The `main()` CLI exits 1 on any error and 0 otherwise.
  Every later task runs it.

- [ ] **Step 1: Write the failing test**

Create `tests/test_validate.py`:

```python
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import validate


def _write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def _msgs(root: Path):
    return [m for _sev, m in validate.validate(root)]


GOOD = """---
id: project-demo
title: Demo
type: project
domain: ai-marketing-gtm
status: draft
created: 2026-11-19
updated: 2026-11-19
company: Acme
category: workflow
url: https://example.com
claims: []
sources:
  - url: https://example.com
    title: "Demo"
    accessed: 2026-11-19
    via: webfetch
---

# Demo

A fact [1].
"""


class ValidateTests(unittest.TestCase):
    def test_clean_record(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            _write(root, "projects/project-demo.md", GOOD)
            self.assertEqual(validate.validate(root), [])

    def test_missing_frontmatter_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            _write(root, "projects/x.md", "# No frontmatter\n")
            out = validate.validate(root)
            self.assertTrue(any(s == "error" and "frontmatter" in m for s, m in out))

    def test_missing_required_field_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            _write(root, "projects/project-demo.md", GOOD.replace("company: Acme\n", ""))
            out = validate.validate(root)
            self.assertTrue(any(s == "error" and "company" in m for s, m in out))

    def test_duplicate_id_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            _write(root, "projects/a.md", GOOD)
            _write(root, "projects/b.md", GOOD)  # same id
            out = validate.validate(root)
            self.assertTrue(any(s == "error" and "duplicate" in m for s, m in out))

    def test_empty_sources_is_warning(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            text = GOOD.replace(
                'sources:\n  - url: https://example.com\n    title: "Demo"\n    accessed: 2026-11-19\n    via: webfetch\n',
                "sources: []\n",
            )
            _write(root, "projects/project-demo.md", text)
            out = validate.validate(root)
            self.assertTrue(any(s == "warning" and "source" in m for s, m in out))

    def test_published_with_no_sources_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            text = GOOD.replace("status: draft\n", "status: published\n").replace(
                'sources:\n  - url: https://example.com\n    title: "Demo"\n    accessed: 2026-11-19\n    via: webfetch\n',
                "sources: []\n",
            )
            _write(root, "projects/project-demo.md", text)
            out = validate.validate(root)
            self.assertTrue(any(s == "error" and "source" in m for s, m in out))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_validate -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'validate'`.

- [ ] **Step 3: Write `scripts/validate.py`**

```python
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
        if line.startswith("- "):
            cur = {}
            items.append(cur)
            key, _, val = line[2:].partition(":")
            cur[key.strip()] = _scalar(val)
        elif line.startswith("  ") and cur is not None:
            key, _, val = line.lstrip().partition(":")
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
            for ref in fm.get(ref_k) or []:
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_validate -v`
Expected: PASS (6 tests).

- [ ] **Step 5: Commit**

```bash
git add scripts/validate.py tests/test_validate.py
git commit -m "feat: add validation script"
```

---

### Task 14: Sample content (real, via opencli)

**Files:**
- Create: `projects/project-<a>.md`, `projects/project-<b>.md`, `problems/problem-<one>.md`, `solutions/solution-<one>.md`

**Interfaces:**
- Consumes: templates, skills, `scripts/validate.py`, `domains/ai-marketing-gtm/README.md`
- Produces: a small real sample set that passes `validate.py`.

- [ ] **Step 1: Choose two real projects**

Pick two real AI Marketing/GTM products with official pages in the
`ai-marketing-gtm` domain. Prefer ones with a public blog or docs page that
states the use case (for example an LLM content-generation tool and an LLM
workflow tool). Confirm the `category` fits the taxonomy.

- [ ] **Step 2: Capture evidence with opencli**

For each project, use `opencli` (or `WebFetch` fallback) to open the official
page and capture: the product's stated use case, the vendor's own claims, and
the page URL + title + access date. Record `via: opencli` or `via: webfetch`.

Do **not** invent numbers. If a claim is not on the page, do not record it.

- [ ] **Step 3: Write the two project records**

Fill `templates/project.md` for each. Record official claims as claims. Cite
facts with `[1]`. Leave `status: draft`.

- [ ] **Step 4: Write one problem record**

From the two projects, derive one real marketing problem (for example "slow
content production"). Fill `templates/problem.md`; cite the project records.

- [ ] **Step 5: Write one solution record**

Describe the pattern both projects share (or one of them), filling
`templates/solution.md` with `solves` and `used_by` pointing at the real ids.

- [ ] **Step 6: Run validation**

Run: `python3 scripts/validate.py`
Expected: `OK` (no errors).

- [ ] **Step 7: Commit**

```bash
git add projects/ problems/ solutions/
git commit -m "docs: add sample content set"
```

---

### Task 15: Consistency review and gaps list

**Files:**
- Create: `research/research-consistency-review.md` (or add a "Remaining gaps" section to README)

**Interfaces:**
- Produces: the final gaps list required by the spec.

- [ ] **Step 1: Run the full validation and skill dry-runs**

```bash
python3 scripts/validate.py
ls -R skills/
```

- [ ] **Step 2: Review against the spec**

Check each spec section maps to a deliverable. Confirm: eight principles are in
README/CLAUDE; four templates exist; five skills exist; validation covers six
checks; sample set is real and cited.

- [ ] **Step 3: Write the gaps list**

Write `research/research-consistency-review.md` listing remaining gaps, for
example: which domain sub-categories still have no sample record, which skill
has not been exercised on real data, whether a comparison report template is
needed, and whether `via` capture is consistent.

- [ ] **Step 4: Commit**

```bash
git add research/research-consistency-review.md
git commit -m "docs: add consistency review and gaps list"
```

---

## Self-Review Notes

- Spec coverage: Tasks 1-4 (foundation docs), Task 5 (taxonomy), Task 6 (templates), Tasks 7-12 (skills), Task 13 (validation), Tasks 14-15 (sample + review). All six documentation topics (positioning, scope/boundaries, taxonomy, content guidelines, evaluation criteria, maintenance policy) are placed in README/CONTRIBUTING/GOVERNANCE/domain README.
- The sample content (Task 14) is intentionally workflow-shaped because the exact facts depend on live opencli capture; the structure and evidence rules are fully specified.
