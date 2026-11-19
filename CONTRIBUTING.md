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
