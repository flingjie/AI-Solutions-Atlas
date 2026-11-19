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
