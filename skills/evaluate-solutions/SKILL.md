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
