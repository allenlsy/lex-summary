#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
test_dir=$(mktemp -d "${TMPDIR:-/tmp}/lex-tldr-new-post-duplicate-test.XXXXXX")
trap 'rm -rf "$test_dir"' EXIT

title='456 - Ukraine, War, Peace, Putin, Trump, NATO, and Freedom'

cd "$repo_dir"
POSTS_DIR="$test_dir" POST_DATE=2026-08-16 just new-post "$title" en >/dev/null

if POSTS_DIR="$test_dir" POST_DATE=2026-08-17 just new-post "$title" en >/dev/null 2>&1; then
  echo "FAIL: duplicate episode-language variant was accepted" >&2
  exit 1
fi

post_count=$(find "$test_dir" -type f -name '*.md' | wc -l | tr -d ' ')
if [ "$post_count" -ne 1 ]; then
  echo "FAIL: duplicate attempt changed the number of posts" >&2
  exit 1
fi

echo "PASS: new-post rejects a duplicate episode-language variant"
