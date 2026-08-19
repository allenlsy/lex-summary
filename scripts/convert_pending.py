#!/usr/bin/env python3
"""Convert pending summary files into Jekyll posts.

Reads Markdown files from pending/<collection_id>/ (or --pending), derives the
episode id, title, language, and original link, and writes a Jekyll post into
_posts/.

Conventions:
- The directory name under pending/ is the collection id (e.g. lex-fridman).
- Language is detected from the file name language mark or the CJK share of
  the content, defaulting to English.
- The title comes from the first top-level heading, falling back to the file
  name; ALL-CAPS transcript titles are normalized.
- The episode must exist in the verified video table (VIDEOS); unknown
  episodes are rejected so converted posts always carry an episode number.
- Dry-run by default; never overwrites an existing post; source files are
  moved to pending/processed/ only on --apply.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PENDING_DIR = REPO_DIR / "pending"
POSTS_DIR = REPO_DIR / "_posts"
COLLECTIONS_FILE = REPO_DIR / "_data" / "collections.yml"
PROCESSED_DIR_NAME = "processed"

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


def ascii_slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


CJK_RE = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF]")
EPISODE_RE = re.compile(r"^\s*(\d+)")
LANG_MARK_RE = re.compile(r"[-_.](zh-cn|zh|cn|en|中文)([-_.]|$)", re.IGNORECASE)
PODCAST_URL = "https://lexfridman.com/podcast"
YOUTUBE_WATCH_URL = "https://www.youtube.com/watch?v={video_id}"

LOWERCASE_WORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on",
    "or", "the", "to", "with", "vs",
}

ACRONYMS = {
    "AGI", "AI", "API", "CEO", "CFO", "CPU", "EU", "GPU", "LLM", "LLMS",
    "ML", "MIT", "NASA", "NLP", "TV", "UK", "USA",
}


class ConversionError(Exception):
    """Raised when a pending file cannot be converted into a Jekyll post."""


def slugify(text: str) -> str:
    """Lowercase ASCII slug; keep CJK characters; collapse separators."""
    slug = []
    for char in text.strip().lower():
        if char.isascii():
            if char.isalnum():
                slug.append(char)
            else:
                slug.append("-")
        elif CJK_RE.match(char):
            slug.append(char)
        else:
            slug.append("-")
    return re.sub(r"-{2,}", "-", "".join(slug)).strip("-")


def known_collection_ids() -> set[str]:
    """Read collection ids from _data/collections.yml."""
    ids: set[str] = set()
    try:
        text = COLLECTIONS_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ids
    for line in text.splitlines():
        match = re.match(r"^\s*- id:\s*(.+?)\s*$", line)
        if match:
            ids.add(match.group(1))
    return ids


def title_case(text: str) -> str:
    """Headline capitalization for ALL-CAPS titles: major words title-cased,
    short connector words lowered, and known acronyms preserved."""
    words = text.split()
    result = []
    for index, word in enumerate(words):
        lowered = word.lower()
        if lowered in LOWERCASE_WORDS and index != 0 and index != len(words) - 1:
            result.append(lowered)
        elif word.upper() in ACRONYMS:
            result.append(word.upper())
        else:
            result.append(word[0].upper() + word[1:].lower() if word else word)
    return " ".join(result)


def detect_language(path: Path, content: str) -> str:
    """Chinese from the file name language mark or CJK ratio, otherwise English."""
    match = LANG_MARK_RE.search(path.stem)
    if match and match.group(1).lower() in {"zh", "zh-cn", "cn", "中文"}:
        return "cn"
    if match and match.group(1).lower() == "en":
        return "en"
    chars = [c for c in content if not c.isspace()]
    if not chars:
        return "en"
    cjk = sum(1 for c in chars if CJK_RE.match(c))
    return "cn" if cjk / len(chars) > 0.3 else "en"


def extract_title(path: Path, content: str) -> str:
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and len(stripped) > 2:
            raw = stripped[2:].strip()
            cleaned = re.sub(r"^(transcript paraphrase|transcript|summary|paraphrase)\s*:\s*", "", raw, flags=re.IGNORECASE)
            if cleaned:
                if any(char.islower() for char in cleaned):
                    return cleaned
                return title_case(cleaned)
    return path.stem


def episode_number(title: str) -> str | None:
    match = EPISODE_RE.match(title)
    return match.group(1) if match else None


def article_body_from_filename(path: Path) -> str:
    """Strip language marks and common boilerplate words from the file name."""
    stem = LANG_MARK_RE.sub(" ", path.stem)
    for word in ("lexfridman.com", "lexfridman", "transcript", "summary"):
        stem = re.sub(r"[-_.]?" + re.escape(word) + r"[-_.]?", " ", stem, flags=re.IGNORECASE)
    return " ".join(stem.split())


def significant_words(text: str) -> set[str]:
    """Lowercased content words of at least three letters, minus connectors."""
    words = set()
    for token in re.findall(r"[A-Za-z]{3,}", text.lower()):
        if token not in LOWERCASE_WORDS:
            words.add(token)
    return words


DEFAULT_API_URL = "http://localhost:1234/v1"
DEFAULT_MODEL = "qwen/qwen3.6-35b-a3b"


def summarize_excerpt(
    content: str,
    language: str,
    api_url: str | None,
    model: str,
    api_key: str | None = None,
) -> str | None:
    """Two-sentence summary via an OpenAI-compatible chat endpoint; None on failure."""
    if not api_url:
        return None
    import urllib.request

    lang_label = "Chinese" if language == "cn" else "English"
    prompt = (
        f"Write a {lang_label} summary of this blog post in 2 sentences "
        f"(about 40-80 words for English, 60-100 Chinese characters). Capture the "
        f"guest, episode topic, and key themes. Output only the summary text.\n\n"
        f"{content[:3000]}"
    )
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 200,
    }
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    try:
        request = urllib.request.Request(
            api_url.rstrip("/") + "/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"].strip()
        return text or None
    except Exception:
        return None


def extract_excerpt(content: str) -> str | None:
    """First substantive paragraph for the excerpt front matter: skip YAML front
    matter, empty lines, headings, separators, and standalone bold labels."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "---" or stripped.startswith("#"):
            continue
        if stripped.startswith("**") and stripped.endswith("**"):
            if not re.search(r"[.!?。！？]\s*$", stripped):
                continue
        plain = re.sub(r"^[*_>\s]+", "", stripped)
        plain = re.sub(r"[*_`]+", "", plain)
        plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", plain)
        plain = plain.strip()
        if len(plain) < 20:
            continue
        return plain
    return None


def parse_podcast_episodes(html: str) -> list[tuple[str, str]]:
    """Extract (title, youtube_id) pairs from the lexfridman.com/podcast page."""
    pairs = []
    for part in html.split('<div class="episode-item">')[1:]:
        title_match = re.search(r'<div class="episode-title">(.*?)</div>', part, re.S)
        youtube_match = re.search(r"youtube\.com/watch\?v=([\w-]+)", part)
        if title_match and youtube_match:
            title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip()
            if title:
                pairs.append((title, youtube_match.group(1)))
    return pairs


def match_episode(title: str, episodes: list[tuple[str, str]], extra_title: str = "") -> tuple[str, str] | None:
    """Best title match by shared significant words; requires at least two."""
    title_words = significant_words(title) | significant_words(extra_title)
    if not title_words:
        return None
    best = None
    best_score = 1
    for episode_title, video_id in episodes:
        score = len(title_words & significant_words(episode_title))
        if score > best_score:
            best = (episode_title, video_id)
            best_score = score
    return best


def parse_youtube_number(page: str) -> tuple[str, str] | None:
    """Return (episode_number, official_title) from a YouTube watch page title."""
    match = re.search(
        r"<title>(.*?)\| Lex Fridman Podcast #(\d+)\s*[-–—]?\s*YouTube</title>",
        page,
        re.IGNORECASE | re.S,
    )
    if not match:
        return None
    return match.group(2), match.group(1).strip().replace("&amp;", "&").strip()


def fetch_url(url: str) -> str | None:
    """Fetch a URL with a browser-like user agent; None on any failure."""
    import urllib.request

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"},
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception:
        return None


def resolve_episode_number(
    title: str, path: Path, page_html: str | None = None
) -> tuple[str | None, str | None]:
    """Look up the episode number and official title online.

    Returns (episode_number, official_title); both None when the episode cannot
    be found on the podcast page. The file name contributes significant words,
    so Chinese variants of the same episode match through their shared slug.
    Never blocks on user input.
    """
    page = page_html if page_html is not None else fetch_url(PODCAST_URL)
    if page is None:
        return None, None
    episodes = parse_podcast_episodes(page)
    if not episodes:
        return None, None
    match = match_episode(title, episodes, article_body_from_filename(path))
    if match is None:
        return None, None
    episode_title, video_id = match
    youtube_page = fetch_url(YOUTUBE_WATCH_URL.format(video_id=video_id))
    if youtube_page is None:
        return None, episode_title
    parsed = parse_youtube_number(youtube_page)
    if parsed is None:
        return None, episode_title
    number, official_title = parsed
    return number, official_title or episode_title


def find_video(title: str, path: Path) -> tuple[object | None, str | None]:
    """Locate the verified video entry: numbered titles check the table,
    unnumbered titles match the file name against verified unnumbered entries."""
    number = episode_number(title)
    if number:
        video = VIDEOS.get(f"#{number}")
        return video, number
    name_slug = article_body_from_filename(path)
    for key, video in VIDEOS.items():
        if not key.startswith("#") and ascii_slugify(video.title) == name_slug:
            return video, None
    return None, None


def next_variant_rank(article_id: str) -> int:
    ranks = []
    for post in POSTS_DIR.glob("*.md"):
        try:
            text = post.read_text(encoding="utf-8")
        except OSError:
            continue
        match = re.search(r"^article_id:\s*(.+?)\s*$", text, re.MULTILINE)
        if not match or match.group(1).strip() != article_id:
            continue
        rank_match = re.search(r"^variant_rank:\s*(\d+)\s*$", text, re.MULTILINE)
        if rank_match:
            ranks.append(int(rank_match.group(1)))
    return max(ranks, default=0) + 1


def build_front_matter(
    *,
    title: str,
    date: str,
    article_id: str,
    article_title: str,
    collection_id: str,
    language: str,
    variant_rank: int,
    permalink: str,
    original_link: str | None = None,
    excerpt: str | None = None,
) -> str:
    def quote(value: str) -> str:
        return f'"{value}"'

    return "\n".join(
        [
            "---",
            "layout: post",
            f"title: {quote(title)}",
            f"date: {date} 09:00:00 +0000",
            f"article_id: {article_id}",
            f"article_title: {quote(article_title)}",
            f"collection_id: {collection_id}",
            f"language: {language}",
            f"variant_rank: {variant_rank}",
            *([f"original_link: {quote(original_link)}"] if original_link else []),
            *([f"excerpt: {quote(excerpt)}"] if excerpt else []),
            f"permalink: {quote(permalink)}",
            "---",
            "",
        ]
    )


def convert_file(
    path: Path,
    collection_id: str,
    *,
    apply: bool,
    page_html: str | None = None,
    api_url: str | None = None,
    model: str = DEFAULT_MODEL,
    api_key: str | None = None,
) -> tuple[str, str] | None:
    """Convert one pending file. Returns (destination, post_text); None when the
    destination already exists.

    The episode number comes from the heading, the verified video table, the
    lexfridman.com/podcast page, or a user prompt, in that order.
    """
    content = path.read_text(encoding="utf-8")
    language = detect_language(path, content)
    heading_title = extract_title(path, content)

    title_number = episode_number(heading_title)
    video = VIDEOS.get(f"#{title_number}") if title_number else None

    # Unnumbered episodes: the verified table, then the podcast page, then the user
    table_entry = None
    online_number = None
    official_title = None
    if not title_number:
        table_entry, _ = find_video(heading_title, path)
        if table_entry is None:
            online_number, official_title = resolve_episode_number(heading_title, path, page_html)
            if online_number is None:
                try:
                    online_number = input(
                        f"Enter the Lex Fridman episode number for '{heading_title}': "
                    ).strip()
                except EOFError:
                    online_number = ""
                if not online_number:
                    raise ConversionError(
                        f"could not determine an episode number for '{heading_title}'"
                    )

    if title_number:
        body = heading_title[len(title_number):]
        article_id = f"{title_number}-{slugify(body)}"
    elif table_entry is not None:
        article_id = slugify(article_body_from_filename(path))
    else:
        article_id = f"{online_number}-{slugify(article_body_from_filename(path))}"

    article_title = video.title if video else (
        f"{online_number} - {official_title}" if online_number and official_title else heading_title
    )
    if language == "en":
        title = video.title if video else (
            f"{online_number} - {official_title}" if online_number and official_title else heading_title
        )
    else:
        title = heading_title
        if online_number and not title_number:
            title = f"{online_number} - {title}"
    permalink = f"/articles/{article_id}/{language}/"

    # Strip the first top-level heading from the body, if it was used as the title
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.strip().startswith("# "):
            body_text = "\n".join(lines[index + 1:]).strip() + "\n"
            break
    else:
        body_text = content.strip() + "\n"

    date = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")
    variant_rank = next_variant_rank(article_id)
    destination = POSTS_DIR / f"{date}-{article_id}-{language}.md"

    source_video = video or table_entry
    original_link = f"{YOUTUBE_BASE}{source_video.youtube_id}" if source_video else None

    if destination.exists():
        return None

    post_text = (
        build_front_matter(
            title=title,
            date=date,
            article_id=article_id,
            article_title=article_title,
            collection_id=collection_id,
            language=language,
            variant_rank=variant_rank,
            permalink=permalink,
            original_link=original_link,
            excerpt=summarize_excerpt(content, language, api_url, model, api_key)
            or extract_excerpt(content),
        )
        + "\n"
        + body_text
    )
    return str(destination.relative_to(REPO_DIR)), post_text


def convert_main(args: argparse.Namespace) -> int:
    pending = args.pending
    if not pending.is_dir():
        print(f"ERROR: pending folder not found: {pending}", file=sys.stderr)
        return 1

    known = known_collection_ids()
    files = sorted(pending.rglob("*.md")) + sorted(pending.rglob("*.txt"))
    files = [f for f in files if PROCESSED_DIR_NAME not in f.parts]

    if not files:
        print("No pending files found.")
        return 0

    converted = 0
    skipped_existing = 0
    unknown_collections = set()

    for path in files:
        if args.collection:
            collection_id = args.collection
        else:
            relative = path.relative_to(pending)
            if len(relative.parts) > 1:
                collection_id = relative.parts[0]
            else:
                print(
                    f"SKIP {path}: place files in pending/<collection>/ to pick a collection",
                    file=sys.stderr,
                )
                continue
        if collection_id not in known:
            unknown_collections.add(collection_id)

        try:
            result = convert_file(
                path,
                collection_id,
                apply=args.apply,
                api_url=args.api_url,
                model=args.model,
                api_key=args.api_key,
            )
        except ConversionError as error:
            print(f"SKIP {path.name}: {error}", file=sys.stderr)
            continue
        if result is None:
            skipped_existing += 1
            print(f"SKIP {path.name}: destination already exists")
            continue
        destination, post_text = result

        if args.apply:
            (REPO_DIR / destination).write_text(post_text, encoding="utf-8")
            processed_dir = pending / PROCESSED_DIR_NAME
            processed_dir.mkdir(exist_ok=True)
            path.rename(processed_dir / path.name)
        else:
            print(f"WOULD CREATE {destination} from {path}")

        converted += 1

    for collection_id in sorted(unknown_collections):
        print(
            f"WARNING: collection '{collection_id}' is not in _data/collections.yml; "
            f"add it (and a landing page under collections/) before publishing",
            file=sys.stderr,
        )

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(
        f"{mode}: {converted} converted, {skipped_existing} skipped (existing), "
        f"{len(unknown_collections)} unknown collection(s)"
    )
    return 0



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pending",
        type=Path,
        default=DEFAULT_PENDING_DIR,
        help=f"pending folder (default: {DEFAULT_PENDING_DIR})",
    )
    parser.add_argument(
        "--collection",
        help="override the collection id (defaults to the subfolder name)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write posts and move source files; default is dry-run",
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"OpenAI-compatible endpoint for excerpt summaries (default: {DEFAULT_API_URL})",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"model name for excerpt summaries (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="bearer token for the OpenAI-compatible endpoint",
    )
    return parser.parse_args()


def main() -> int:
    return convert_main(parse_args())


if __name__ == "__main__":
    raise SystemExit(main())

