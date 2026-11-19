---
name: analyze-problems
description: >
  Derive a real marketing/GTM problem from projects and discussions and create
  a `problems/` record. Use when asked to "find the problem this tool solves"
  or "analyze a pain point". Keeps fact/inferred/assumption separate and cites
  project records.
---

# analyze-problems

## Purpose

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
