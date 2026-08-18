#!/usr/bin/env python3
"""Convert pending summary files into Jekyll posts.

Reads Markdown files from Pending/<collection_id>/ (or --pending), derives the
episode id, title, and language, and writes a Jekyll post into _posts/.

Conventions:
- The directory name under Pending/ is the collection id (e.g. lex-fridman).
- Language is detected from the file name suffix (cn/zh/中文) or from the
  share of CJK characters in the content, defaulting to English.
- The title comes from the first top-level heading in the file, falling back
  to the file name.
- An episode number at the start of the title becomes the article id prefix.
- Dry-run by default; never overwrites an existing post; source files are
  moved to Pending/processed/ only on --apply.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parents[1]
DEFAULT_PENDING_DIR = REPO_DIR / "Pending"
POSTS_DIR = REPO_DIR / "_posts"
COLLECTIONS_FILE = REPO_DIR / "_data" / "collections.yml"
PROCESSED_DIR_NAME = "processed"

CJK_RE = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF]")
EPISODE_RE = re.compile(r"^\s*(\d+)")
LANG_MARK_RE = re.compile(r"[-_.](zh-cn|zh|cn|en|中文)([-_.]|$)", re.IGNORECASE)

LOWERCASE_WORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "of", "on",
    "or", "the", "to", "with", "vs",
}

ACRONYMS = {
    "AGI", "AI", "API", "CEO", "CFO", "CPU", "EU", "GPU", "LLM", "LLMS",
    "ML", "MIT", "NASA", "NLP", "TV", "UK", "USA",
}


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


def derive_article_id(title: str, path: Path) -> str:
    """Numbered titles use the number plus slug; otherwise derive the id from the
    file name so language variants of the same episode share one article_id."""
    number = episode_number(title)
    if number:
        body = title[len(number):]
        return f"{number}-{slugify(body)}"
    return slugify(article_body_from_filename(path))


def article_body_from_filename(path: Path) -> str:
    """Strip language marks and common boilerplate words from the file name."""
    stem = LANG_MARK_RE.sub(" ", path.stem)
    for word in ("lexfridman.com", "lexfridman", "transcript", "summary"):
        stem = re.sub(r"[-_.]?" + re.escape(word) + r"[-_.]?", " ", stem, flags=re.IGNORECASE)
    return " ".join(stem.split())


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
            f"permalink: {quote(permalink)}",
            "---",
            "",
        ]
    )


def convert_file(path: Path, collection_id: str, *, apply: bool) -> tuple[str, str] | None:
    """Convert one pending file. Returns (destination, post_text) or None to skip."""
    content = path.read_text(encoding="utf-8")
    language = detect_language(path, content)
    title = extract_title(path, content)
    article_id = derive_article_id(title, path)
    article_title = title
    permalink = f"/articles/{article_id}/{language}/"

    # Strip the first top-level heading from the body, if it was used as the title
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.strip().startswith("# "):
            body = "\n".join(lines[index + 1:]).strip() + "\n"
            break
    else:
        body = content.strip() + "\n"

    date = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")
    variant_rank = next_variant_rank(article_id)
    destination = POSTS_DIR / f"{date}-{article_id}-{language}.md"

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
        )
        + "\n"
        + body
    )
    return str(destination.relative_to(REPO_DIR)), post_text


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert pending summaries into Jekyll posts."
    )
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
    args = parser.parse_args()

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
                    f"SKIP {path}: place files in Pending/<collection>/ to pick a collection",
                    file=sys.stderr,
                )
                continue
        if collection_id not in known:
            unknown_collections.add(collection_id)

        result = convert_file(path, collection_id, apply=args.apply)
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


if __name__ == "__main__":
    sys.exit(main())
