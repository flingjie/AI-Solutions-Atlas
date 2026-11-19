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
