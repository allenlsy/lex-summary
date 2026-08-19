#!/usr/bin/env python3
"""Tests for scripts/convert_excerpt.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import convert_excerpt as ce


class UpdateExcerptTests(unittest.TestCase):
    def test_replaces_existing_excerpt(self) -> None:
        text = (
            "---\nlayout: post\narticle_id: x\nexcerpt: \"Old summary\"\n"
            "permalink: /articles/x/en/\n---\n\nBody."
        )
        result = ce.update_excerpt(text, "New summary")
        self.assertIn('excerpt: "New summary"', result)
        self.assertNotIn("Old summary", result)

    def test_inserts_when_missing(self) -> None:
        text = "---\nlayout: post\narticle_id: x\npermalink: /articles/x/en/\n---\n\nBody."
        result = ce.update_excerpt(text, "New summary")
        self.assertIn('excerpt: "New summary"', result)
        self.assertIn('excerpt: "New summary"\npermalink:', result)

    def test_malformed_returns_none(self) -> None:
        self.assertIsNone(ce.update_excerpt("no front matter here", "summary"))

    def test_escapes_quotes(self) -> None:
        text = "---\nlayout: post\npermalink: /articles/x/en/\n---\n\nBody."
        result = ce.update_excerpt(text, 'He said "hello"')
        self.assertIn('excerpt: "He said \\"hello\\""', result)


class DateFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        (self.tmp / "2026-08-17-a-en.md").write_text(
            "---\nlayout: post\nlanguage: en\npermalink: /articles/a/en/\n---\n\nBody A.", encoding="utf-8"
        )
        (self.tmp / "2026-08-18-b-cn.md").write_text(
            "---\nlayout: post\nlanguage: cn\npermalink: /articles/b/cn/\n---\n\n正文。", encoding="utf-8"
        )
        (self.tmp / "2026-09-01-c-en.md").write_text(
            "---\nlayout: post\nlanguage: en\npermalink: /articles/c/en/\n---\n\nBody C.", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_range_filters_posts(self) -> None:
        from unittest import mock

        calls = []
        def fake_summarize(content, language, api_url, model):
            calls.append((language, len(content)))
            return f"Summary for {language}"

        with mock.patch.object(ce, "summarize_excerpt", side_effect=fake_summarize):
            ce.main.__wrapped__ if hasattr(ce.main, "__wrapped__") else None
            # drive main via its internals: rebuild args by patching sys.argv
            import sys
            old_argv = sys.argv
            sys.argv = ["convert_excerpt.py", "--start", "2026-08-17", "--end", "2026-08-18",
                        "--posts-dir", str(self.tmp), "--apply", "--api-url", "http://test/v1"]
            try:
                rc = ce.main()
            finally:
                sys.argv = old_argv
        self.assertEqual(rc, 0)
        self.assertEqual(len(calls), 2)
        langs = [lang for lang, _ in calls]
        self.assertIn("en", langs)
        self.assertIn("cn", langs)
        self.assertEqual(
            (self.tmp / "2026-08-18-b-cn.md").read_text(encoding="utf-8").split("---")[1].lstrip("\n"),
            'layout: post\nlanguage: cn\nexcerpt: "Summary for cn"\npermalink: /articles/b/cn/\n',
        )
        # out-of-range post untouched
        self.assertNotIn("excerpt:", (self.tmp / "2026-09-01-c-en.md").read_text(encoding="utf-8"))

    def test_invalid_dates_rejected(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["convert_excerpt.py", "--start", "not-a-date", "--end", "2026-08-18"]
        try:
            rc = ce.main()
        finally:
            sys.argv = old_argv
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
