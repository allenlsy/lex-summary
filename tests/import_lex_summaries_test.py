import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[1]
SCRIPT = REPO_DIR / "scripts" / "import_lex_summaries.py"


class ImportLexSummariesTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source_dir = self.root / "source"
        self.posts_dir = self.root / "posts"
        self.source_dir.mkdir()
        self.posts_dir.mkdir()

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_source(self, filename, body):
        path = self.source_dir / filename
        path.write_bytes(body)
        return path

    def run_import(self, *extra_args):
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--source-dir",
                str(self.source_dir),
                "--posts-dir",
                str(self.posts_dir),
                *extra_args,
            ],
            capture_output=True,
            text=True,
        )

    def test_apply_preserves_sources_and_imports_language_variants(self):
        sources = {
            "A day in my life | Lex Fridman-en-summary.md": b"English day summary.\n",
            "A day in my life | Lex Fridman-summary.md": b"English day summary.\n",
            "Ilya Sutskever_ Deep Learning _ Lex Fridman Podcast #94-en-summary.md": b"English episode summary.\n",
            "Ilya Sutskever_ Deep Learning _ Lex Fridman Podcast #94-zh-cn-summary.md": "中文节目总结。\n".encode(),
        }
        paths = {name: self.write_source(name, body) for name, body in sources.items()}
        before = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}

        preview = self.run_import()
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(list(self.posts_dir.iterdir()), [])

        result = self.run_import("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Created 3 post(s)", result.stdout)

        day_post = self.posts_dir / "2020-08-27-a-day-in-my-life-en.md"
        en_post = self.posts_dir / "2020-05-08-94-ilya-sutskever-deep-learning-en.md"
        cn_post = self.posts_dir / "2020-05-08-94-ilya-sutskever-deep-learning-cn.md"
        self.assertEqual(sorted(self.posts_dir.iterdir()), sorted([day_post, en_post, cn_post]))
        self.assertTrue(day_post.read_bytes().endswith(sources["A day in my life | Lex Fridman-en-summary.md"]))
        self.assertTrue(en_post.read_bytes().endswith(sources["Ilya Sutskever_ Deep Learning _ Lex Fridman Podcast #94-en-summary.md"]))
        self.assertTrue(cn_post.read_bytes().endswith(sources["Ilya Sutskever_ Deep Learning _ Lex Fridman Podcast #94-zh-cn-summary.md"]))
        self.assertIn("language: cn", cn_post.read_text())
        self.assertIn("variant_rank: 2", cn_post.read_text())
        self.assertIn("original_link: \"https://www.youtube.com/watch?v=13CZPWmke6A\"", cn_post.read_text())

        after = {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()}
        self.assertEqual(after, before)

        repeated = self.run_import("--apply")
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertIn("Created 0 post(s)", repeated.stdout)

    def test_duplicate_language_summaries_get_ordered_specs(self):
        filenames = [
            "Pieter Levels: Programming, Viral AI Startups, and Digital Nomad Life | Lex Fridman Podcast #440-en-summary.md",
            "Pieter Levels: Programming, Viral AI Startups, and Digital Nomad Life | Lex Fridman Podcast #440-zh-Hans-summary.md",
            "Pieter Levels_ Programming, Viral AI Startups, and Digital Nomad Life _ Lex Fridman Podcast #440-en-summary.md",
            "Pieter Levels_ Programming, Viral AI Startups, and Digital Nomad Life _ Lex Fridman Podcast #440-zh-cn-summary.md",
        ]
        for index, filename in enumerate(filenames, start=1):
            self.write_source(filename, f"Summary {index}.\n".encode())

        result = self.run_import("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)

        slug = "440-pieter-levels-programming-viral-ai-startups-and-digital-nomad-life"
        expected = [
            (f"2024-08-20-{slug}-en-short.md", "variant_rank: 1", "  - short"),
            (f"2024-08-20-{slug}-cn-short.md", "variant_rank: 2", "  - short"),
            (f"2024-08-20-{slug}-en-long.md", "variant_rank: 3", "  - long"),
            (f"2024-08-20-{slug}-cn-long.md", "variant_rank: 4", "  - long"),
        ]
        for filename, rank, spec in expected:
            content = (self.posts_dir / filename).read_text()
            self.assertIn(rank, content)
            self.assertIn(spec, content)

    def test_lex_clips_sources_are_excluded(self):
        clip = self.write_source(
            "Advice for machine learning beginners | Andrej Karpathy and Lex Fridman-en-summary.md",
            b"Clip summary.\n",
        )
        episode = self.write_source(
            "Ilya Sutskever_ Deep Learning _ Lex Fridman Podcast #94-en-summary.md",
            b"Podcast summary.\n",
        )
        before = {
            clip.name: hashlib.sha256(clip.read_bytes()).hexdigest(),
            episode.name: hashlib.sha256(episode.read_bytes()).hexdigest(),
        }

        result = self.run_import("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            [path.name for path in self.posts_dir.iterdir()],
            ["2020-05-08-94-ilya-sutskever-deep-learning-en.md"],
        )
        self.assertIn("1 Lex Clips source file(s) excluded", result.stdout)
        after = {
            clip.name: hashlib.sha256(clip.read_bytes()).hexdigest(),
            episode.name: hashlib.sha256(episode.read_bytes()).hexdigest(),
        }
        self.assertEqual(after, before)

    def test_import_removes_leading_generation_boilerplate(self):
        self.write_source(
            "Aella_ Sex Work, OnlyFans, Porn, Escorting, Dating, and Human Sexuality _ Lex Fridman Podcast #358-en-summary.md",
            (
                "**Paraphrased Text in English (Approx. 5,200 words)**\n"
                "*Note: This version is longer than the original, as requested.*\n\n"
                "**Documentary Paraphrase of the Interview**\n"
                "The following is a detailed paraphrase prepared to meet the requested word count.\n\n"
                "Editorial requirements for the generated version:\n"
                "- Preserve all details and examples.\n\n---\n\n"
                "## A real opening\n\nActual article content.\n"
            ).encode(),
        )
        self.write_source(
            "Aella_ Sex Work, OnlyFans, Porn, Escorting, Dating, and Human Sexuality _ Lex Fridman Podcast #358-zh-cn-summary.md",
            (
                "以下是该文本的简体中文准确翻译：\n"
                "**改写后的中文全文（约5,200字）**\n\n"
                "**访谈文本转写 paraphrase**\n"
                "以下为原文经过重构的改写版本，以满足用户要求的字数。\n\n"
                "- 纪录片、新闻报道风格，中立且客观。\n"
                "- 保留所有事实信息与例证。\n"
                "- 深层含义涉及科技伦理。\n"
                "语调保持新闻报道风格。\n\n---\n\n"
                "## 正文开头\n\n真正的文章内容。\n"
            ).encode(),
        )

        result = self.run_import("--apply")
        self.assertEqual(result.returncode, 0, result.stderr)

        en_post = next(self.posts_dir.glob("*-en.md")).read_text()
        cn_post = next(self.posts_dir.glob("*-cn.md")).read_text()
        self.assertNotIn("Paraphrased Text", en_post)
        self.assertNotIn("Note: This version", en_post)
        self.assertNotIn("Documentary Paraphrase", en_post)
        self.assertNotIn("requested word count", en_post)
        self.assertNotIn("Editorial requirements", en_post)
        self.assertNotIn("Preserve all details", en_post)
        self.assertIn("\n## A real opening\n", en_post)
        self.assertNotIn("简体中文准确翻译", cn_post)
        self.assertNotIn("改写后的中文全文", cn_post)
        self.assertNotIn("文本转写", cn_post)
        self.assertNotIn("用户要求", cn_post)
        self.assertNotIn("新闻报道风格", cn_post)
        self.assertNotIn("保留所有事实", cn_post)
        self.assertNotIn("深层含义", cn_post)
        self.assertNotIn("语调保持", cn_post)
        self.assertIn("\n## 正文开头\n", cn_post)

    def test_collision_aborts_before_writing_any_posts(self):
        self.write_source("A day in my life | Lex Fridman-en-summary.md", b"Source body.\n")
        self.write_source(
            "Ilya Sutskever_ Deep Learning _ Lex Fridman Podcast #94-en-summary.md",
            b"Another source body.\n",
        )
        collision = self.posts_dir / "2020-08-27-a-day-in-my-life-en.md"
        collision.write_text("User-owned file.\n")

        result = self.run_import("--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Refusing to overwrite", result.stderr)
        self.assertEqual(collision.read_text(), "User-owned file.\n")
        self.assertEqual(list(self.posts_dir.iterdir()), [collision])


if __name__ == "__main__":
    unittest.main()
