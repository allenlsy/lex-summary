#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
test_dir=$(mktemp -d "${TMPDIR:-/tmp}/lex-tldr-new-post-variant-test.XXXXXX")
trap 'rm -rf "$test_dir"' EXIT

title='456 - Ukraine, War, Peace, Putin, Trump, NATO, and Freedom'
slug='456-ukraine-war-peace-putin-trump-nato-and-freedom'

cd "$repo_dir"
POSTS_DIR="$test_dir" POST_DATE=2026-08-16 just new-post "$title" en >/dev/null
POSTS_DIR="$test_dir" POST_DATE=2026-08-17 just new-post "$title" cn >/dev/null

cn_post="$test_dir/2026-08-17-$slug-cn.md"

if ! grep -Fq 'variant_rank: 2' "$cn_post"; then
  echo "FAIL: second language variant does not receive rank 2" >&2
  exit 1
fi

if ! grep -Fq "article_id: $slug" "$cn_post"; then
  echo "FAIL: second language variant does not reuse the episode ID" >&2
  exit 1
fi

echo "PASS: new-post relates and ranks a second language variant"
