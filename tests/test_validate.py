from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import validate


def _write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def _msgs(root: Path):
    return [m for _sev, m in validate.validate(root)]


GOOD = """---
id: project-demo
title: Demo
type: project
domain: ai-marketing-gtm
status: draft
created: 2026-11-19
updated: 2026-11-19
company: Acme
category: workflow
url: https://example.com
claims: []
sources:
  - url: https://example.com
    title: "Demo"
    accessed: 2026-11-19
    via: webfetch
---

# Demo

A fact [1].
"""

PROJECT = GOOD

PROBLEM = """---
id: problem-demo
title: Demo problem
type: problem
domain: ai-marketing-gtm
status: draft
created: 2026-11-19
updated: 2026-11-19
who: marketing teams
pain_points: []
sources:
  - url: https://example.com
    title: "Demo"
    accessed: 2026-11-19
    via: webfetch
---

# Demo problem
"""


def _solution(solves="problem-demo", used_by="project-demo"):
    return f"""---
id: solution-demo
title: Demo solution
type: solution
domain: ai-marketing-gtm
status: draft
created: 2026-11-19
updated: 2026-11-19
solves: [{solves}]
used_by: [{used_by}]
mechanism: a cited mechanism
limitations: []
sources:
  - url: https://example.com
    title: "Demo"
    accessed: 2026-11-19
    via: webfetch
---

# Demo solution
"""


class ValidateTests(unittest.TestCase):
    def test_clean_record(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            _write(root, "projects/project-demo.md", GOOD)
            self.assertEqual(validate.validate(root), [])

    def test_missing_frontmatter_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            _write(root, "projects/x.md", "# No frontmatter\n")
            out = validate.validate(root)
            self.assertTrue(any(s == "error" and "frontmatter" in m for s, m in out))

    def test_missing_required_field_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            _write(root, "projects/project-demo.md", GOOD.replace("company: Acme\n", ""))
            out = validate.validate(root)
            self.assertTrue(any(s == "error" and "company" in m for s, m in out))

    def test_empty_title_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            _write(root, "projects/project-demo.md", GOOD.replace('title: Demo\n', 'title: ""\n'))
            out = validate.validate(root)
            self.assertTrue(any(s == "error" and "title" in m for s, m in out))

    def test_duplicate_id_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            _write(root, "projects/a.md", GOOD)
            _write(root, "projects/b.md", GOOD)  # same id
            out = validate.validate(root)
            self.assertTrue(any(s == "error" and "duplicate" in m for s, m in out))

    def test_empty_sources_is_warning(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            text = GOOD.replace(
                'sources:\n  - url: https://example.com\n    title: "Demo"\n    accessed: 2026-11-19\n    via: webfetch\n',
                "sources: []\n",
            )
            _write(root, "projects/project-demo.md", text)
            out = validate.validate(root)
            self.assertTrue(any(s == "warning" and "source" in m for s, m in out))

    def test_published_with_no_sources_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            text = GOOD.replace("status: draft\n", "status: published\n").replace(
                'sources:\n  - url: https://example.com\n    title: "Demo"\n    accessed: 2026-11-19\n    via: webfetch\n',
                "sources: []\n",
            )
            _write(root, "projects/project-demo.md", text)
            out = validate.validate(root)
            self.assertTrue(any(s == "error" and "source" in m for s, m in out))

    def test_valid_references_pass(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            (root / "problems").mkdir()
            (root / "solutions").mkdir()
            _write(root, "projects/project-demo.md", PROJECT)
            _write(root, "problems/problem-demo.md", PROBLEM)
            _write(root, "solutions/solution-demo.md", _solution())
            out = validate.validate(root)
            self.assertEqual(out, [])

    def test_reference_to_missing_id_is_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            (root / "problems").mkdir()
            (root / "solutions").mkdir()
            _write(root, "projects/project-demo.md", PROJECT)
            _write(root, "problems/problem-demo.md", PROBLEM)
            _write(root, "solutions/solution-demo.md", _solution(solves="problem-missing"))
            out = validate.validate(root)
            self.assertTrue(any(s == "error" and "missing id" in m for s, m in out))

    def test_solves_pointing_at_project_is_type_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            (root / "problems").mkdir()
            (root / "solutions").mkdir()
            _write(root, "projects/project-demo.md", PROJECT)
            _write(root, "problems/problem-demo.md", PROBLEM)
            _write(root, "solutions/solution-demo.md", _solution(solves="project-demo"))
            out = validate.validate(root)
            self.assertTrue(any(
                s == "error" and "expects problem" in m and "is project" in m for s, m in out
            ))

    def test_renamed_file_with_stable_id_resolves(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "projects").mkdir()
            (root / "problems").mkdir()
            (root / "solutions").mkdir()
            _write(root, "projects/renamed-file.md", PROJECT)  # id is still project-demo
            _write(root, "problems/problem-demo.md", PROBLEM)
            _write(root, "solutions/solution-demo.md", _solution())
            out = validate.validate(root)
            self.assertEqual(out, [])


if __name__ == "__main__":
    unittest.main()
