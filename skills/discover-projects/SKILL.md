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
