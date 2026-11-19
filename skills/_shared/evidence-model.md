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
