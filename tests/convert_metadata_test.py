#!/usr/bin/env python3
"""Tests for admin/convert_metadata.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import convert_metadata as cm


class ProgressBarTests(unittest.TestCase):
    def test_format(self) -> None:
        bar = cm.progress_bar(0, 70)
        self.assertEqual(bar, "\r[" + "-" * 28 + "]   0.0% (0/70)")
        full = cm.progress_bar(70, 70)
        self.assertIn("[#" * 1, full)
        self.assertIn("100.0% (70/70)", full)

    def test_zero_total(self) -> None:
        self.assertIn("(0/0)", cm.progress_bar(0, 0))


class UpdateExcerptTests(unittest.TestCase):
    def test_replaces_existing_excerpt(self) -> None:
        text = (
            "---\nlayout: post\narticle_id: x\nexcerpt: \"Old summary\"\n"
            "permalink: /articles/x/en/\n---\n\nBody."
        )
        result = cm.update_excerpt(text, "New summary")
        self.assertIn('excerpt: "New summary"', result)
        self.assertNotIn("Old summary", result)

    def test_inserts_when_missing(self) -> None:
        text = "---\nlayout: post\narticle_id: x\npermalink: /articles/x/en/\n---\n\nBody."
        result = cm.update_excerpt(text, "New summary")
        self.assertIn('excerpt: "New summary"', result)
        self.assertIn('excerpt: "New summary"\npermalink:', result)

    def test_malformed_returns_none(self) -> None:
        self.assertIsNone(cm.update_excerpt("no front matter here", "summary"))

    def test_escapes_quotes(self) -> None:
        text = "---\nlayout: post\npermalink: /articles/x/en/\n---\n\nBody."
        result = cm.update_excerpt(text, 'He said "hello"')
        self.assertIn('excerpt: "He said \\"hello\\""', result)

    def test_update_field_replaces_title(self) -> None:
        text = "---\nlayout: post\ntitle: \"Old\"\npermalink: /articles/x/en/\n---\n\nBody."
        result = cm.update_field(text, "title", "New")
        self.assertIn('title: "New"', result)
        self.assertNotIn('"Old"', result)

    def test_update_field_inserts_title_before_permalink(self) -> None:
        text = "---\nlayout: post\narticle_id: x\npermalink: /articles/x/en/\n---\n\nBody."
        result = cm.update_field(text, "title", "New")
        self.assertIn('title: "New"', result)
        self.assertLess(result.index('title: "New"'), result.index("permalink:"))


class DateFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        (self.tmp / "2026-08-17-a-en.md").write_text(
            "---\nlayout: post\nlanguage: en\npermalink: /articles/a/en/\n---\n\n"
            "This is the first substantive paragraph of the English post body.\n",
            encoding="utf-8",
        )
        (self.tmp / "2026-08-18-b-cn.md").write_text(
            "---\nlayout: post\nlanguage: cn\npermalink: /articles/b/cn/\n---\n\n"
            "这是中文正文的第一段实质性内容，用于测试摘要回填。\n",
            encoding="utf-8",
        )
        (self.tmp / "2026-09-01-c-en.md").write_text(
            "---\nlayout: post\nlanguage: en\npermalink: /articles/c/en/\n---\n\n"
            "This is the first substantive paragraph of the out-of-range post body.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_range_filters_posts(self) -> None:
        import sys

        old_argv = sys.argv
        sys.argv = ["convert_metadata.py", "--start", "2026-08-17", "--end", "2026-08-18",
                    "--posts-dir", str(self.tmp), "--apply"]
        try:
            rc = cm.main()
        finally:
            sys.argv = old_argv
        self.assertEqual(rc, 0)
        # in-range posts get their missing excerpt filled from the first paragraph
        self.assertIn(
            'excerpt: "This is the first substantive paragraph of the English post body."',
            (self.tmp / "2026-08-17-a-en.md").read_text(encoding="utf-8"),
        )
        self.assertIn(
            "excerpt: \"这是中文正文的第一段实质性内容",
            (self.tmp / "2026-08-18-b-cn.md").read_text(encoding="utf-8"),
        )
        # out-of-range post untouched
        self.assertNotIn("excerpt:", (self.tmp / "2026-09-01-c-en.md").read_text(encoding="utf-8"))

    def test_existing_excerpt_kept(self) -> None:
        import sys

        (self.tmp / "2026-08-17-a-en.md").write_text(
            "---\nlayout: post\nlanguage: en\nexcerpt: \"Existing\"\npermalink: /articles/a/en/\n---\n\n"
            "This is the first substantive paragraph of the English post body.\n",
            encoding="utf-8",
        )
        old_argv = sys.argv
        sys.argv = ["convert_metadata.py", "--posts-dir", str(self.tmp), "--apply"]
        try:
            rc = cm.main()
        finally:
            sys.argv = old_argv
        self.assertEqual(rc, 0)
        text = (self.tmp / "2026-08-17-a-en.md").read_text(encoding="utf-8")
        # an existing excerpt is never touched, even though the body changed
        self.assertIn('excerpt: "Existing"', text)
        self.assertNotIn("first substantive paragraph", text.split("---")[1])
        # the excerpt-less cn post still gets its excerpt filled
        self.assertIn("excerpt:", (self.tmp / "2026-08-18-b-cn.md").read_text(encoding="utf-8"))

    def test_api_key_forwarded(self) -> None:
        from unittest import mock
        import sys

        (self.tmp / "2026-08-17-a-cn.md").write_text(
            "---\nlayout: post\nlanguage: cn\narticle_title: \"450 - Bernie Sanders Interview\"\n"
            "permalink: /articles/a/cn/\n---\n\n"
            "这是中文正文的第一段实质性内容，用于测试。\n",
            encoding="utf-8",
        )
        captured = {}
        def fake_translate(title, language, api_url, model, api_key=None):
            captured["key"] = api_key
            return "450 - 伯尼·桑德斯访谈"

        old_argv = sys.argv
        sys.argv = ["convert_metadata.py", "--posts-dir", str(self.tmp), "--apply",
                    "--api-url", "http://test/v1", "--api-key", "secret-token"]
        try:
            with mock.patch.object(cm, "translate_title", side_effect=fake_translate):
                cm.main()
        finally:
            sys.argv = old_argv
        self.assertEqual(captured.get("key"), "secret-token")

    def test_invalid_dates_rejected(self) -> None:
        import sys
        old_argv = sys.argv
        sys.argv = ["convert_metadata.py", "--start", "not-a-date", "--end", "2026-08-18"]
        try:
            rc = cm.main()
        finally:
            sys.argv = old_argv
        self.assertEqual(rc, 1)

    def test_omitted_dates_use_defaults(self) -> None:
        import sys

        old_argv = sys.argv
        # no --start/--end: covers all posts up to today
        sys.argv = ["convert_metadata.py", "--posts-dir", str(self.tmp), "--apply"]
        try:
            rc = cm.main()
        finally:
            sys.argv = old_argv
        self.assertEqual(rc, 0)
        # default end date covers 08-17 and 08-18; 09-01 is out of range
        self.assertIn("excerpt:", (self.tmp / "2026-08-18-b-cn.md").read_text(encoding="utf-8"))
        self.assertNotIn("excerpt:", (self.tmp / "2026-09-01-c-en.md").read_text(encoding="utf-8"))


class TitleTranslationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _run(self, argv: list[str]) -> None:
        import sys

        old_argv = sys.argv
        sys.argv = ["convert_metadata.py"] + argv
        try:
            cm.main()
        finally:
            sys.argv = old_argv

    def test_cn_title_translated_from_article_title(self) -> None:
        from unittest import mock

        (self.tmp / "2026-08-17-a-cn.md").write_text(
            "---\nlayout: post\nlanguage: cn\n"
            "title: \"450 - lexfridman.com-x-transcript-zh-cn-summary\"\n"
            "article_title: \"450 - Bernie Sanders Interview\"\n"
            "permalink: /articles/a/cn/\n---\n\n正文。",
            encoding="utf-8",
        )
        with mock.patch.object(cm, "translate_title", return_value="450 - 伯尼·桑德斯访谈") as tt:
            self._run(["--posts-dir", str(self.tmp), "--apply", "--api-url", "http://test/v1"])
        tt.assert_called_once()
        self.assertEqual(tt.call_args.args[0], "450 - Bernie Sanders Interview")
        text = (self.tmp / "2026-08-17-a-cn.md").read_text(encoding="utf-8")
        self.assertIn('title: "450 - 伯尼·桑德斯访谈"', text)

    def test_chinese_article_title_not_translated(self) -> None:
        from unittest import mock

        (self.tmp / "2026-08-17-a-cn.md").write_text(
            "---\nlayout: post\nlanguage: cn\n"
            "title: \"450 - 伯尼·桑德斯访谈\"\n"
            "article_title: \"450 - 伯尼·桑德斯访谈\"\n"
            "permalink: /articles/a/cn/\n---\n\n正文。",
            encoding="utf-8",
        )
        with mock.patch.object(cm, "translate_title", return_value="X") as tt:
            self._run(["--posts-dir", str(self.tmp), "--apply", "--api-url", "http://test/v1"])
        tt.assert_not_called()
        text = (self.tmp / "2026-08-17-a-cn.md").read_text(encoding="utf-8")
        self.assertIn('title: "450 - 伯尼·桑德斯访谈"', text)

    def test_en_title_untouched(self) -> None:
        from unittest import mock

        (self.tmp / "2026-08-17-a-en.md").write_text(
            "---\nlayout: post\nlanguage: en\n"
            "title: \"450 - Bernie Sanders Interview\"\n"
            "article_title: \"450 - Bernie Sanders Interview\"\n"
            "permalink: /articles/a/en/\n---\n\nBody.",
            encoding="utf-8",
        )
        with mock.patch.object(cm, "translate_title", return_value="X") as tt:
            self._run(["--posts-dir", str(self.tmp), "--apply", "--api-url", "http://test/v1"])
        tt.assert_not_called()
        text = (self.tmp / "2026-08-17-a-en.md").read_text(encoding="utf-8")
        self.assertIn('title: "450 - Bernie Sanders Interview"', text)


if __name__ == "__main__":
    unittest.main()
