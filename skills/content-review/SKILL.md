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
