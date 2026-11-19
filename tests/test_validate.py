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


if __name__ == "__main__":
    unittest.main()
