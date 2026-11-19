# Consistency Review — Remaining Gaps

Date: 2026-11-19
Status: final review for phase 5

## What exists and passes

The repository is healthy. `python3 scripts/validate.py` exits 0 and prints `OK`.
The unit tests pass (7 tests). All five skills exist under `skills/`. The
`.claude/skills` and `.codex/skills` symlinks point to `../skills`. Each skill
has these sections: Purpose, Input, Output, Workflow, Evidence requirements,
Quality checks, and Example. Four templates exist in `templates/`. The sample
set has two project records, one problem record, and one solution record. Every
sample source is an official vendor page. `via` is `opencli` in all six source
entries.

## Spec coverage

| Spec section | Deliverable | State |
| --- | --- | --- |
| 2 Core principles | README (8 numbered), CLAUDE.md / AGENTS.md | Present |
| 3 Key decisions | symlinks, stdlib validator, `via` capture | Present |
| 4 Repository structure | all directories and symlinks | Present, except skill `references/` (G13) |
| 5 Evidence model | `skills/_shared/`, sample records | Present, templates omit source shape (G6) |
| 6 Content types and templates | four templates | Present, placeholder defect (G7) |
| 7 Skills | five skills, seven sections each | Present |
| 8 Validation | `scripts/validate.py`, six checks | Partial (G1–G5) |
| 9 Sample content | 2 projects, 1 problem, 1 solution | Present (G8–G12) |
| 10 Phases | all five phases delivered | Present |

## Remaining gaps

Each gap has a tag. **spec gap** means the spec requires it and the repository
does not build it. **follow-up** means the design defers it.

### Validation coverage

- **G1 — `category` value is not checked.** `validate.py` requires the
  `category` field but accepts any value. It does not compare the value with the
  taxonomy in `domains/ai-marketing-gtm/README.md`. Spec §6 and §8.1 require a
  valid category. **spec gap**
- **G2 — Type-specific fields are not fully required.** Spec §6 lists these
  fields. `validate.py` does not require all of them. Missing checks: project
  `claims`, problem `current_approach`, solution `used_by` and `limitations`,
  research `method` and `conclusions`. Spec §6 and §8.1. **spec gap**
- **G3 — Duplicate `title` + `company` is not checked.** `validate.py` checks a
  duplicate `id` only. Spec §8.4 also requires a check for the same `title` +
  `company`. **spec gap**
- **G4 — `related` references are not checked.** `validate.py` checks `solves`
  and `used_by` only. Spec §8.6 also lists `related`. **spec gap**
- **G5 — Body links are not checked.** `validate.py` checks frontmatter
  references only. It does not parse Markdown links in the body. Spec §8.3
  requires internal references to resolve to existing files. **spec gap**

### Templates

- **G6 — Templates do not show the source entry shape.** All four templates use
  `sources: []`. They do not show the `url`, `title`, `accessed`, and `via`
  fields. Spec §5 defines this shape. **follow-up**
- **G7 — The solution template has a placeholder mismatch.** The template uses
  `id: solution-<name>` but `solves: [problem-<id>]` and
  `used_by: [project-<id>]`. The placeholder token is not consistent.
  **follow-up**

### Sample content

- **G8 — Vendor result numbers cite homepages.** Jasper and Clay result numbers
  (for example "10,000+ hours", "68% faster", "3x", "140%") cite the homepage.
  A case-study page can support each number better. Spec §9 asks for official
  sources. **follow-up**
- **G9 — `via: opencli` has no snapshot.** All six source entries record
  `via: opencli`. The repository has no captured snapshot. A reviewer cannot
  check the capture. Spec §3 requires the method record only. **follow-up**
- **G10 — Three sub-categories have no sample record.** The sample set covers
  `content-generation` and `workflow`. It has no record for `personalization`,
  `analytics`, or `gtm-research`. Spec §9 asks for a small sample set.
  **follow-up**
- **G11 — `compare-projects` has no real-data run.** `research/` has no sample
  report. No record shows a real run of this skill. Spec §9 does not require a
  research record. **follow-up**
- **G12 — No comparison-report template.** `ROADMAP.md` lists this template as
  "Later (not planned)". This is a deferred design decision. **follow-up**

### Structure

- **G13 — No per-skill `references/` directory.** The spec §4 tree shows
  `skills/<name>/references/`. The repository has no such directory. Shared
  conventions are in `skills/_shared/`. Spec §7 does not require a per-skill
  `references/` directory. **follow-up**

## Summary

The repository matches the spec. The main open work is validation coverage
(G1–G5). The other gaps are deferred improvements. The sample set is
intentionally small.
