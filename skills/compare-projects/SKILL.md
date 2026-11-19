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
