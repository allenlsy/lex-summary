#!/usr/bin/env python3
"""Safely import local Lex Fridman summary Markdown files into Jekyll posts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_SOURCE_DIR = Path(
    "/Users/allenlsy/Library/Mobile Documents/com~apple~CloudDocs/ytbrf/Lex Fridman"
)
DEFAULT_POSTS_DIR = Path(__file__).resolve().parents[1] / "_posts"
YOUTUBE_BASE = "https://www.youtube.com/watch?v="


@dataclass(frozen=True)
class Video:
    title: str
    upload_date: str
    youtube_id: str
    already_imported: bool = False


VIDEOS = {
    "#94": Video("94 - Ilya Sutskever: Deep Learning", "2020-05-08", "13CZPWmke6A"),
    "#333": Video("333 - Andrej Karpathy: Tesla AI, Self-Driving, Optimus, Aliens, and AGI", "2022-10-29", "cdiD-9MMpb0"),
    "#358": Video("358 - Aella: Sex Work, OnlyFans, Porn, Escorting, Dating, and Human Sexuality", "2023-02-10", "cFSrxSBrgSc"),
    "#389": Video("389 - Benjamin Netanyahu: Israel, Palestine, Power, Corruption, Hate, and Peace", "2023-07-12", "XpC7SVDXimg"),
    "#390": Video("390 - Yuval Noah Harari: Human Nature, Intelligence, Power, and Conspiracies", "2023-07-17", "Mde2q7GFCrw"),
    "#415": Video("415 - Serhii Plokhy: History of Ukraine, Russia, Soviet Union, KGB, Nazis & War", "2024-03-04", "qa-wl8_wpZA"),
    "#416": Video("416 - Yann LeCun: Meta AI, Open Source, Limits of LLMs, AGI & the Future of AI", "2024-03-07", "5t1vTLU7s40"),
    "#424": Video("424 - Bassem Youssef: Israel-Palestine, Gaza, Hamas, Middle East, Satire & Fame", "2024-04-05", "sG8u6owzad4"),
    "#432": Video("432 - Kevin Spacey: Power, Controversy, Betrayal, Truth & Love in Film and Life", "2024-06-05", "XJTMQtE-MIo"),
    "#435": Video("435 - Andrew Huberman: Focus, Controversy, Politics, and Relationships", "2024-06-27", "ZIyB9e_7a4c"),
    "#440": Video("440 - Pieter Levels: Programming, Viral AI Startups, and Digital Nomad Life", "2024-08-20", "oFtjKbXKqbg"),
    "#452": Video("452 - Dario Amodei: Anthropic CEO on Claude, AGI & the Future of AI & Humanity", "2024-11-11", "ugvHCXCOmm4"),
    "#456": Video("456 - Ukraine, War, Peace, Putin, Trump, NATO, and Freedom", "2025-01-05", "u321m25rKXc", already_imported=True),
    "#458": Video("458 - Marc Andreessen: Trump, Power, Tech, AI, Immigration & Future of America", "2025-01-26", "OHWnPOKh_S0"),
    "#459": Video("459 - DeepSeek, China, OpenAI, NVIDIA, xAI, TSMC, Stargate, and AI Megaclusters", "2025-02-03", "_1f-o0nqpEI"),
    "#464": Video("464 - Dave Smith: Israel, Hamas, Ukraine, Russia, Conspiracies & Antisemitism", "2025-04-08", "1V0bJfqEaa4"),
    "#471": Video("471 - Sundar Pichai: CEO of Google and Alphabet", "2025-06-05", "9V6tWC4CdFQ"),
    "#472": Video("472 - Terence Tao: Hardest Problems in Mathematics, Physics & the Future of AI", "2025-06-14", "HUkBz-cdB-k"),
    "#474": Video("474 - DHH: Future of Programming, AI, Ruby on Rails, Productivity & Parenting", "2025-07-12", "vagyIcmIGOQ"),
    "#475": Video("475 - Demis Hassabis: Future of AI, Simulating Reality, Physics and Video Games", "2025-07-23", "-HzgcbRXUK8"),
    "#477": Video("477 - Keyu Jin: China's Economy, Tariffs, Trade, Trump, Communism & Capitalism", "2025-08-13", "y3yAVZk3tyA"),
    "#481": Video("481 - Norman Ohler: Hitler, Nazis, Drugs, WW2, Blitzkrieg, LSD, MKUltra & CIA", "2025-09-19", "SvKv7D4pBjE"),
    "#484": Video("484 - Dan Houser: GTA, Red Dead Redemption, Rockstar, Absurd & Future of Gaming", "2025-10-31", "o3gbXDjNWyI"),
    "#490": Video("490 - State of AI in 2026: LLMs, Coding, Scaling Laws, China, Agents, GPUs, AGI", "2026-01-31", "EV7WhVT270Q"),
    "#491": Video("491 - OpenClaw: The Viral AI Agent that Broke the Internet - Peter Steinberger", "2026-02-12", "YFjfBk8HI5o"),
    "#494": Video("494 - Jensen Huang: NVIDIA - The $4 Trillion Company & the AI Revolution", "2026-03-23", "vif8NQcjVf0"),
    "1984 by George Orwell _ Lex Fridman": Video("1984 by George Orwell", "2023-01-08", "7Sk6lTLSZcA"),
    "A day in my life | Lex Fridman": Video("A day in my life", "2020-08-27", "0m3hGZvD-0s"),
}

EXCLUDED_LEX_CLIPS = {
    "A machine learning approach to stock trading | Richard Craib and Lex Fridman",
    "Advice for machine learning beginners | Andrej Karpathy and Lex Fridman",
    "Banks are corrupt: Money is all that matters | Matthew Cox and Lex Fridman",
    "Google CEO: Will AGI be created by 2030? | Sundar Pichai and Lex Fridman",
    "Mark Zuckerberg's disagreement with OpenAI and Google on AI | Lex Fridman Podcast Clips",
    "Terence Tao on future of AI in mathematics | Terence Tao and Lex Fridman",
    "The secret to Elon Musk's productivity | Walter Isaacson and Lex Fridman",
}

LANGUAGE_SUFFIXES = {
    "en-us": "en",
    "en": "en",
    "zh-cn": "cn",
    "zh-Hans": "cn",
    "auto": "en",
}
LANGUAGE_ORDER = {"en": 0, "cn": 1}
SPEC_ORDER = {None: 0, "short": 0, "long": 1}


@dataclass(frozen=True)
class SourceSummary:
    path: Path
    key: str
    base_title: str
    language: str
    spec: str | None
    body: bytes
    digest: str


@dataclass(frozen=True)
class PlannedPost:
    source: SourceSummary
    target: Path
    payload: bytes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE_DIR)
    parser.add_argument("--posts-dir", type=Path, default=DEFAULT_POSTS_DIR)
    parser.add_argument("--apply", action="store_true", help="Create posts after a successful preflight")
    return parser.parse_args()


def slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def parse_filename(path: Path) -> tuple[str, str]:
    name = path.name
    for suffix, language in LANGUAGE_SUFFIXES.items():
        marker = f"-{suffix}-summary{path.suffix}"
        if name.endswith(marker):
            return name[: -len(marker)], language
    marker = f"-summary{path.suffix}"
    if name.endswith(marker):
        return name[: -len(marker)], "en"
    raise ValueError(f"Unsupported summary filename: {path.name}")


def source_key(base_title: str) -> str:
    match = re.search(r"Lex Fridman Podcast #(\d+)", base_title)
    return f"#{match.group(1)}" if match else base_title


def source_spec(key: str, base_title: str) -> str | None:
    if key != "#440":
        return None
    return "short" if " | Lex Fridman Podcast #440" in base_title else "long"


def plain_markdown_line(line: str) -> str:
    plain = line.strip()
    plain = re.sub(r"^[#>*_\s]+", "", plain)
    plain = re.sub(r"[*_\s]+$", "", plain)
    return plain.strip()


def is_generation_boilerplate(line: str) -> bool:
    plain = plain_markdown_line(line)
    lower = plain.lower()
    english_prefixes = (
        "paraphrase of transcript",
        "paraphrased text",
        "paraphrased transcript",
        "documentary paraphrase",
        "comprehensive documentary paraphrase",
        "summary of the transcript",
        "summary of the conversation",
        "overview of the conversation: a third-person analysis",
        "here is a summary of the provided transcript",
        "here is the translation of the provided text",
        "documentary report:",
        "documentary feature:",
    )
    chinese_prefixes = (
        "以下是该文本的简体中文准确翻译",
        "以下是对",
        "改写后的",
        "改写版访谈",
        "转录文本",
        "重述文稿",
        "全面转述",
        "纪录片报告：",
        "纪录片专题：",
        "综合纪实概述：",
        "对话概述：第三人称分析",
        "人工智能前沿发展综述",
    )
    return (
        lower.startswith(english_prefixes)
        or plain.startswith(chinese_prefixes)
        or "paraphrase" in lower
        or "改写" in plain
        or "转写" in plain
        or "第三人称叙述" in plain
        or "第三人称改写" in plain
        or "纪录片式摘要" in plain
        or plain.endswith("对话摘要")
        or (lower.startswith("the following is") and "word" in lower)
        or lower.startswith("this detailed paraphrase")
        or plain.startswith("本次详尽的转述")
        or plain.startswith("本转述")
        or (plain.startswith("以下为原文") and "用户要求" in plain)
        or plain.startswith("语调遵循新闻报道员")
        or plain.startswith("语调保持新闻报道风格")
        or plain.startswith("最终版本超过最低字数要求")
    )


def is_generation_note(line: str) -> bool:
    plain = plain_markdown_line(line)
    lower = plain.lower()
    return (
        lower.startswith("note: this version")
        or lower.startswith("documentary, neutral, journalistic tone")
        or lower.startswith("editorial requirements for the generated version")
        or lower.startswith("prepared in accordance with the user")
        or lower.startswith("the tone adheres to")
        or lower.startswith("the tone remains journalistic")
        or lower.startswith("the final version exceeds")
        or lower.startswith("word count:")
        or bool(re.match(r"^\(?approx\.?.*words", lower))
        or (plain.startswith("（约") and "目标范围" in plain)
        or plain.startswith("纪录片风格，中立、新闻纪实语气")
        or plain.startswith("根据用户指令整理")
        or plain.startswith("语调遵循新闻报道员")
        or plain.startswith("最终版本超过最低字数要求")
        or (
            plain.startswith("-")
            and any(
                marker in lower
                for marker in (
                    "third-person",
                    "documentary",
                    "retains all details",
                    "preserve all details",
                    "completeness over brevity",
                    "final output",
                    "original text",
                    "target:",
                    "factual details",
                    "illustrations and examples",
                    "opinions and stated beliefs",
                    "conclusions drawn",
                    "logical structure",
                    "emotional undercurrents",
                    "implications",
                    "纪录片",
                    "新闻报道风格",
                    "保留所有",
                    "完整性",
                    "最终输出",
                    "原始文本",
                    "原文",
                    "目标",
                    "事实信息",
                    "例证",
                    "观点",
                    "结论",
                    "结构",
                    "情感",
                    "影响",
                    "深层含义",
                )
            )
        )
    )


def clean_source_body(body: bytes) -> bytes:
    text = body.decode("utf-8")
    lines = text.splitlines(keepends=True)
    index = 0
    while index < len(lines) and not lines[index].strip():
        index += 1
    if index == len(lines) or not is_generation_boilerplate(lines[index]):
        return body

    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.strip() == "---":
            index += 1
        elif is_generation_boilerplate(line) or is_generation_note(line):
            index += 1
        else:
            break
    return "".join(lines[index:]).lstrip("\r\n").encode("utf-8")


def discover_sources(source_dir: Path) -> tuple[list[SourceSummary], int]:
    if not source_dir.is_dir():
        raise ValueError(f"Source directory does not exist: {source_dir}")

    paths = sorted([*source_dir.glob("*summary.md"), *source_dir.glob("*summary.markdown")])
    if not paths:
        raise ValueError(f"No summary Markdown files found in {source_dir}")

    discovered = []
    excluded_count = 0
    for path in paths:
        base_title, language = parse_filename(path)
        key = source_key(base_title)
        if key in EXCLUDED_LEX_CLIPS:
            excluded_count += 1
            continue
        if key not in VIDEOS:
            raise ValueError(f"No verified video metadata for {path.name}")
        body = path.read_bytes()
        discovered.append(
            SourceSummary(
                path=path,
                key=key,
                base_title=base_title,
                language=language,
                spec=source_spec(key, base_title),
                body=body,
                digest=hashlib.sha256(body).hexdigest(),
            )
        )
    return discovered, excluded_count


def deduplicate_sources(sources: list[SourceSummary]) -> tuple[list[SourceSummary], int]:
    unique = {}
    duplicates = 0
    for source in sources:
        identity = (source.key, source.language, source.spec)
        existing = unique.get(identity)
        if existing is None:
            unique[identity] = source
        elif existing.digest == source.digest:
            duplicates += 1
        else:
            raise ValueError(
                "Multiple different summaries map to the same variant: "
                f"{existing.path.name} and {source.path.name}"
            )
    return list(unique.values()), duplicates


def make_front_matter(video: Video, source: SourceSummary, rank: int) -> bytes:
    slug = slugify(video.title)
    suffix = f"/{source.spec}/" if source.spec else "/"
    lines = [
        "---",
        "layout: post",
        f"title: {json.dumps(video.title, ensure_ascii=False)}",
        f"date: {video.upload_date} 09:00:00 +0000",
        f"article_id: {slug}",
        f"article_title: {json.dumps(video.title, ensure_ascii=False)}",
        "collection_id: lex-fridman",
        f"language: {source.language}",
    ]
    if source.spec:
        lines.extend(["spec:", f"  - {source.spec}"])
    lines.extend(
        [
            f"variant_rank: {rank}",
            f"original_link: {json.dumps(YOUTUBE_BASE + video.youtube_id)}",
            f"permalink: /articles/{slug}/{source.language}{suffix}",
            "---",
            "",
        ]
    )
    return ("\n".join(lines) + "\n").encode()


def plan_posts(sources: list[SourceSummary], posts_dir: Path) -> tuple[list[PlannedPost], int]:
    unique, duplicate_count = deduplicate_sources(sources)
    grouped = {}
    for source in unique:
        grouped.setdefault(source.key, []).append(source)

    plans = []
    for key, variants in sorted(grouped.items()):
        video = VIDEOS[key]
        if video.already_imported:
            continue
        variants.sort(
            key=lambda source: (
                SPEC_ORDER[source.spec],
                LANGUAGE_ORDER.get(source.language, 99),
                source.path.name,
            )
        )
        for rank, source in enumerate(variants, start=1):
            slug = slugify(video.title)
            spec_suffix = f"-{source.spec}" if source.spec else ""
            filename = f"{video.upload_date}-{slug}-{source.language}{spec_suffix}.md"
            payload = make_front_matter(video, source, rank) + clean_source_body(source.body)
            plans.append(PlannedPost(source, posts_dir / filename, payload))
    return plans, duplicate_count


def preflight(plans: list[PlannedPost]) -> tuple[list[PlannedPost], int]:
    to_create = []
    unchanged = 0
    for plan in plans:
        if not plan.target.exists():
            to_create.append(plan)
        elif plan.target.read_bytes() == plan.payload:
            unchanged += 1
        else:
            raise ValueError(f"Refusing to overwrite existing file: {plan.target}")
    return to_create, unchanged


def main() -> int:
    args = parse_args()
    try:
        sources, excluded_count = discover_sources(args.source_dir)
        plans, duplicate_count = plan_posts(sources, args.posts_dir)
        to_create, unchanged = preflight(plans)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    for plan in to_create:
        print(f"CREATE {plan.target.name} <- {plan.source.path.name}")
    print(
        f"Preflight: {len(sources)} source file(s), {excluded_count} Lex Clips source file(s) excluded, "
        f"{duplicate_count} exact duplicate(s), "
        f"{unchanged} already imported, {len(to_create)} to create"
    )

    if not args.apply:
        print("Dry run only; pass --apply to create posts.")
        return 0

    args.posts_dir.mkdir(parents=True, exist_ok=True)
    created = 0
    try:
        for plan in to_create:
            with plan.target.open("xb") as target:
                target.write(plan.payload)
            created += 1
    except FileExistsError as error:
        print(f"ERROR: Refusing to overwrite file created during import: {error.filename}", file=sys.stderr)
        return 1

    print(f"Created {created} post(s); source files were not modified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
