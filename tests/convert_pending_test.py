#!/usr/bin/env python3
"""Tests for the pending-summary conversion mode of import_lex_summaries.py."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import import_lex_summaries as cp


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
        self.assertIn("language: cn", post_text)
        self.assertIn("collection_id: lex-fridman", post_text)
        self.assertIn("variant_rank: 1", post_text)
        self.assertIn("permalink: \"/articles/416-yann-lecun-大语言模型的局限/cn/\"", post_text)
        self.assertNotIn("# 416", post_text.split("---")[2])

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

    def test_unknown_episode_rejected(self) -> None:
        source = self.tmp / "khabib-summary.md"
        source.write_text("# TRANSCRIPT PARAPHRASE: KHABIB NURMAGOMEDOV\n\nBody.", encoding="utf-8")
        with self.assertRaises(cp.ConversionError):
            cp.convert_file(source, "lex-fridman", apply=False)

    def test_destination_resolves_within_posts_dir(self) -> None:
        source = self.tmp / "494-jensen.md"
        source.write_text("# 494 - Jensen Huang\n\nBody.", encoding="utf-8")
        destination, _ = cp.convert_file(source, "lex-fridman", apply=False)
        self.assertEqual((cp.REPO_DIR / destination).parent, cp.POSTS_DIR)

    def test_skips_existing_destination(self) -> None:
        source = self.tmp / "494-jensen.md"
        source.write_text("# 494 - Jensen Huang\n\nBody.", encoding="utf-8")
        destination = cp.POSTS_DIR / "2026-08-17-494-jensen-huang-en.md"
        destination.write_text("existing", encoding="utf-8")
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
