#!/usr/bin/env python3
"""Tests for the pending-summary conversion mode of import_lex_summaries.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import convert_pending as cp


class SlugifyTests(unittest.TestCase):
    def test_ascii_slug(self) -> None:
        self.assertEqual(cp.slugify("Yann LeCun: Meta AI, AGI & the Future"), "yann-lecun-meta-ai-agi-the-future")

    def test_keeps_cjk(self) -> None:
        self.assertEqual(cp.slugify("深度学习的局限"), "深度学习的局限")

    def test_collapses_separators(self) -> None:
        self.assertEqual(cp.slugify("A  B---C"), "a-b-c")


class LanguageTests(unittest.TestCase):
    def test_lang_mark_in_middle(self) -> None:
        self.assertEqual(
            cp.detect_language(Path("khabib-transcript-zh-cn-summary.md"), "any text"), "cn"
        )
        self.assertEqual(
            cp.detect_language(Path("khabib-transcript-en-summary.md"), "any text"), "en"
        )

    def test_cjk_ratio(self) -> None:
        content = "这是中文摘要，关于人工智能的对话。This is the summary."
        self.assertEqual(cp.detect_language(Path("416-xxx.md"), content), "cn")

    def test_english_default(self) -> None:
        self.assertEqual(cp.detect_language(Path("416-xxx.md"), "Plain english summary."), "en")


class TitleCaseTests(unittest.TestCase):
    def test_transcript_prefix_stripped(self) -> None:
        content = "# TRANSCRIPT PARAPHRASE: KHABIB NURMAGOMEDOV ON DAGHESTAN, COMBAT SPORTS\n\nbody"
        self.assertEqual(
            cp.extract_title(Path("x.md"), content),
            "Khabib Nurmagomedov on Daghestan, Combat Sports",
        )

    def test_keeps_episode_number(self) -> None:
        content = "# 416 - YANN LECUN: LIMITS OF LLMS\n\nbody"
        self.assertEqual(cp.extract_title(Path("x.md"), content), "416 - Yann Lecun: Limits of LLMS")

    def test_mixed_case_title_preserved(self) -> None:
        content = "# 416 - Yann LeCun: Limits of LLMs\n\nbody"
        self.assertEqual(cp.extract_title(Path("x.md"), content), "416 - Yann LeCun: Limits of LLMs")


class ExcerptTests(unittest.TestCase):
    def test_first_substantive_paragraph(self) -> None:
        content = (
            "# 416 - Yann LeCun\n\n"
            "**Introduction and Episode Highlight**\n\n"
            "The conversation covers the limits of large language models and the future of AI.\n\n"
            "A second paragraph."
        )
        self.assertEqual(
            cp.extract_excerpt(content),
            "The conversation covers the limits of large language models and the future of AI.",
        )

    def test_short_bold_label_skipped(self) -> None:
        content = "**Introduction**\n\nThis is the real summary paragraph with enough length.\n"
        self.assertEqual(cp.extract_excerpt(content), "This is the real summary paragraph with enough length.")

    def test_cjk_paragraph(self) -> None:
        content = "## 1. 引言\n\n这是关于人工智能未来发展的实质性摘要段落，包含足够长的中文内容用于列表页展示。\n"
        self.assertEqual(
            cp.extract_excerpt(content),
            "这是关于人工智能未来发展的实质性摘要段落，包含足够长的中文内容用于列表页展示。",
        )

    def test_bold_numbered_heading_skipped(self) -> None:
        content = (
            "**1. The Historical Arc of Unification in Physics**\n\n"
            "The trajectory of modern physics is fundamentally characterized by a centuries-long pursuit.\n"
        )
        self.assertEqual(
            cp.extract_excerpt(content),
            "The trajectory of modern physics is fundamentally characterized by a centuries-long pursuit.",
        )

    def test_none_when_only_short_lines(self) -> None:
        self.assertIsNone(cp.extract_excerpt("# Only heading\n\n**Label**\n"))


class ConvertTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.old_posts = cp.POSTS_DIR
        self.old_repo = cp.REPO_DIR
        cp.POSTS_DIR = self.tmp / "_posts"
        cp.POSTS_DIR.mkdir()
        cp.REPO_DIR = self.tmp

    def tearDown(self) -> None:
        cp.POSTS_DIR = self.old_posts
        cp.REPO_DIR = self.old_repo
        self._tmp.cleanup()

    def test_front_matter_fields(self) -> None:
        source = self.tmp / "416-yann-cn.md"
        source.write_text(
            "# 416 - Yann LeCun：大语言模型的局限\n\n这是正文。", encoding="utf-8"
        )
        result = cp.convert_file(source, "lex-fridman", apply=False)
        self.assertIsNotNone(result)
        destination, post_text = result
        self.assertIn("416-yann-lecun-大语言模型的局限", destination)
        self.assertIn('title: "416 - Yann LeCun：大语言模型的局限"', post_text)
        self.assertIn(
            'article_title: "416 - Yann LeCun: Meta AI, Open Source, Limits of LLMs, AGI & the Future of AI"',
            post_text,
        )
        self.assertIn("language: cn", post_text)
        self.assertIn("collection_id: lex-fridman", post_text)
        self.assertIn("variant_rank: 1", post_text)
        self.assertIn("permalink: \"/articles/416-yann-lecun-大语言模型的局限/cn/\"", post_text)
        self.assertNotIn("# 416", post_text.split("---")[2])

    def test_english_title_uses_table_title(self) -> None:
        source = self.tmp / "416-yann-en.md"
        source.write_text("# 416 - Yann LeCun: Limits of LLMs\n\nBody.", encoding="utf-8")
        _, post_text = cp.convert_file(source, "lex-fridman", apply=False)
        self.assertIn(
            'title: "416 - Yann LeCun: Meta AI, Open Source, Limits of LLMs, AGI & the Future of AI"',
            post_text,
        )

    def test_numbered_post_gets_original_link(self) -> None:
        source = self.tmp / "416-yann.md"
        source.write_text("# 416 - Yann LeCun: Limits of LLMs\n\nBody.", encoding="utf-8")
        _, post_text = cp.convert_file(source, "lex-fridman", apply=False)
        self.assertIn('original_link: "https://www.youtube.com/watch?v=5t1vTLU7s40"', post_text)

    def test_verified_unnumbered_post(self) -> None:
        source = self.tmp / "a-day-in-my-life-en-summary.md"
        source.write_text("# A day in my life\n\nBody.", encoding="utf-8")
        result = cp.convert_file(source, "lex-fridman", apply=False)
        self.assertIsNotNone(result)
        _, post_text = result
        self.assertIn("article_id: a-day-in-my-life", post_text)
        self.assertIn('original_link: "https://www.youtube.com/watch?v=0m3hGZvD-0s"', post_text)

    def test_online_episode_resolution(self) -> None:
        from unittest import mock

        podcast_html = (
            '<div class="episode-item"><div class="episode-title">'
            '<a href="#">Khabib Nurmagomedov: Dagestan, MMA, UFC, Islam, Conor, Fedor & Football</a>'
            '</div><div class="vid-materials">'
            '<a href="https://www.youtube.com/watch?v=l6USUAIKJls">Video</a>'
            '</div></div>'
        )
        youtube_html = (
            "<title>Khabib Nurmagomedov: Dagestan, MMA, UFC, Islam, Conor, Fedor &amp; Football "
            "| Lex Fridman Podcast #500 - YouTube</title>"
        )
        source = self.tmp / "khabib-nurmagomedov-summary.md"
        source.write_text("# TRANSCRIPT PARAPHRASE: KHABIB NURMAGOMEDOV ON DAGHESTAN\n\nBody.", encoding="utf-8")
        with mock.patch.object(cp, "fetch_url", return_value=youtube_html):
            result = cp.convert_file(source, "lex-fridman", apply=False, page_html=podcast_html)
        self.assertIsNotNone(result)
        _, post_text = result
        self.assertIn("article_id: 500-khabib-nurmagomedov", post_text)
        self.assertIn(
            'article_title: "500 - Khabib Nurmagomedov: Dagestan, MMA, UFC, Islam, Conor, Fedor & Football"',
            post_text,
        )
        self.assertIn(
            'title: "500 - Khabib Nurmagomedov: Dagestan, MMA, UFC, Islam, Conor, Fedor & Football"',
            post_text,
        )
        self.assertIn("permalink: \"/articles/500-khabib-nurmagomedov/en/\"", post_text)

    def test_prompt_for_episode_number(self) -> None:
        from unittest import mock

        source = self.tmp / "mystery-episode.md"
        source.write_text("# A Mystery Conversation\n\nBody.", encoding="utf-8")
        with mock.patch("builtins.input", return_value="501"):
            result = cp.convert_file(source, "lex-fridman", apply=False, page_html="")
        self.assertIsNotNone(result)
        _, post_text = result
        self.assertIn("article_id: 501-mystery-episode", post_text)

    def test_api_summary_used_for_excerpt(self) -> None:
        from unittest import mock

        class FakeResponse:
            def __init__(self, data):
                self._data = data
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self):
                return self._data

        def fake_urlopen(request, timeout=0):
            return FakeResponse(
                b'{"choices": [{"message": {"content": "API generated summary text."}}]}'
            )

        source = self.tmp / "416-yann.md"
        source.write_text("# 416 - Yann LeCun: Limits of LLMs\n\nBody with enough length to have a fallback excerpt.", encoding="utf-8")
        with mock.patch("urllib.request.urlopen", side_effect=fake_urlopen):
            _, post_text = cp.convert_file(source, "lex-fridman", apply=False, api_url="http://localhost:1234/v1")
        self.assertIn('excerpt: "API generated summary text."', post_text)

    def test_api_failure_falls_back_to_extract(self) -> None:
        from unittest import mock

        source = self.tmp / "416-yann.md"
        source.write_text(
            "# 416 - Yann LeCun: Limits of LLMs\n\n**1. A Bold Heading**\n\nThe conversation covers the limits of large language models and the future of AI systems.\n",
            encoding="utf-8",
        )
        with mock.patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
            _, post_text = cp.convert_file(source, "lex-fridman", apply=False, api_url="http://localhost:1234/v1")
        self.assertIn("The conversation covers the limits of large language models", post_text)

    def test_eof_without_number_raises(self) -> None:
        from unittest import mock

        source = self.tmp / "mystery-episode.md"
        source.write_text("# A Mystery Conversation\n\nBody.", encoding="utf-8")
        with mock.patch("builtins.input", side_effect=EOFError):
            with self.assertRaises(cp.ConversionError):
                cp.convert_file(source, "lex-fridman", apply=False, page_html="")

    def test_destination_resolves_within_posts_dir(self) -> None:
        source = self.tmp / "494-jensen.md"
        source.write_text("# 494 - Jensen Huang\n\nBody.", encoding="utf-8")
        destination, _ = cp.convert_file(source, "lex-fridman", apply=False)
        self.assertEqual((cp.REPO_DIR / destination).parent, cp.POSTS_DIR)

    def test_skips_existing_destination(self) -> None:
        source = self.tmp / "494-jensen.md"
        source.write_text("# 494 - Jensen Huang\n\nBody.", encoding="utf-8")
        destination, _ = cp.convert_file(source, "lex-fridman", apply=False)
        self.assertIsNotNone(destination)
        (cp.REPO_DIR / destination).write_text("existing", encoding="utf-8")
        self.assertIsNone(cp.convert_file(source, "lex-fridman", apply=False))

    def test_variant_rank_increments(self) -> None:
        (cp.POSTS_DIR / "2026-01-01-416-x-en.md").write_text(
            "---\nlayout: post\narticle_id: 416-x\nvariant_rank: 2\n---\n",
            encoding="utf-8",
        )
        source = self.tmp / "416-x-cn.md"
        source.write_text("# 416 - X\n\n正文。", encoding="utf-8")
        _, post_text = cp.convert_file(source, "lex-fridman", apply=False)
        self.assertIn("variant_rank: 3", post_text)


if __name__ == "__main__":
    unittest.main()
