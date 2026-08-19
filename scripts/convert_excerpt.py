#!/usr/bin/env python3
"""Regenerate post excerpts for a date range using an OpenAI-compatible API.

Posts are matched by the YYYY-MM-DD prefix of their file name inside _posts/.
Each post body is summarized into a two-sentence excerpt (language follows the
post) and written to the front matter, replacing any existing excerpt.
Dry-run by default; pass --apply to write. Summaries that fail stay untouched.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

from convert_pending import DEFAULT_API_URL, DEFAULT_MODEL, summarize_excerpt

REPO_DIR = Path(__file__).resolve().parents[1]
POSTS_DIR = REPO_DIR / "_posts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--start",
        help="start date YYYY-MM-DD (inclusive); defaults to the earliest post",
    )
    parser.add_argument(
        "--end",
        help="end date YYYY-MM-DD (inclusive); defaults to today",
    )
    parser.add_argument(
        "--api-url",
        default=DEFAULT_API_URL,
        help=f"OpenAI-compatible endpoint (default: {DEFAULT_API_URL})",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"model name (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="bearer token for the OpenAI-compatible endpoint",
    )
    parser.add_argument(
        "--override",
        action="store_true",
        help="regenerate excerpts that already exist; default keeps them",
    )
    parser.add_argument(
        "--posts-dir",
        type=Path,
        default=POSTS_DIR,
        help=f"posts folder (default: {POSTS_DIR})",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write the new excerpts; default is dry-run",
    )
    return parser.parse_args()


def update_excerpt(text: str, excerpt: str) -> str | None:
    """Replace or insert the excerpt line in the front matter."""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm_lines = parts[1].rstrip("\n").splitlines()
    line = f"excerpt: {json.dumps(excerpt, ensure_ascii=False)}"
    for index, fm_line in enumerate(fm_lines):
        if fm_line.startswith("excerpt:"):
            fm_lines[index] = line
            break
    else:
        index = next(
            (n for n, fm_line in enumerate(fm_lines) if fm_line.startswith("permalink:")),
            len(fm_lines),
        )
        fm_lines.insert(index, line)
    return "---" + "\n".join(fm_lines) + "\n---" + parts[2]


def main() -> int:
    args = parse_args()
    try:
        start = date.fromisoformat(args.start) if args.start else date.min
        end = date.fromisoformat(args.end) if args.end else date.today()
    except ValueError as error:
        print(f"ERROR: invalid date: {error}", file=sys.stderr)
        return 1
    if start > end:
        print("ERROR: --start must be on or before --end", file=sys.stderr)
        return 1

    matched = 0
    updated = 0
    skipped_existing = 0
    skipped = 0
    for post in sorted(args.posts_dir.glob("*.md")):
        post_date = post.name[:10]
        if not (start.isoformat() <= post_date <= end.isoformat()):
            continue
        matched += 1
        text = post.read_text(encoding="utf-8")
        parts = text.split("---", 2)
        if len(parts) < 3:
            print(f"SKIP {post.name}: malformed front matter", file=sys.stderr)
            skipped += 1
            continue
        if not args.override and re.search(r"^excerpt:\s*\S", parts[1], re.MULTILINE):
            skipped_existing += 1
            continue
        language = "cn" if re.search(r"^language:\s*cn\s*$", parts[1], re.MULTILINE) else "en"
        summary = summarize_excerpt(
            parts[2].strip(), language, args.api_url, args.model, args.api_key
        )
        if not summary:
            print(f"SKIP {post.name}: summary failed", file=sys.stderr)
            skipped += 1
            continue
        new_text = update_excerpt(text, summary.strip())
        if new_text is None:
            print(f"SKIP {post.name}: malformed front matter", file=sys.stderr)
            skipped += 1
            continue
        if args.apply:
            post.write_text(new_text, encoding="utf-8")
        else:
            print(f"WOULD UPDATE {post.name}")
        updated += 1

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(
        f"{mode}: {matched} posts in range, {updated} updated, "
        f"{skipped_existing} skipped (existing excerpt), {skipped} skipped (error)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
