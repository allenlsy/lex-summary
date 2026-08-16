#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
test_dir=$(mktemp -d "${TMPDIR:-/tmp}/lex-tldr-new-post-test.XXXXXX")
trap 'rm -rf "$test_dir"' EXIT

title='456 - Ukraine, War, Peace, Putin, Trump, NATO, and Freedom'
slug='456-ukraine-war-peace-putin-trump-nato-and-freedom'
post="$test_dir/2026-08-16-$slug-en.md"

cd "$repo_dir"
POSTS_DIR="$test_dir" POST_DATE=2026-08-16 \
  just new-post "$title" en

if [ ! -f "$post" ]; then
  echo "FAIL: new-post did not create $post" >&2
  exit 1
fi

for expected in \
  'title: "456 - Ukraine, War, Peace, Putin, Trump, NATO, and Freedom"' \
  "article_id: $slug" \
  'article_title: "456 - Ukraine, War, Peace, Putin, Trump, NATO, and Freedom"' \
  'collection_id: practice-notes' \
  'language: en' \
  'variant_rank: 1' \
  "permalink: /articles/$slug/en/" \
  'Write the summary here.'
do
  if ! grep -Fq "$expected" "$post"; then
    echo "FAIL: generated post is missing: $expected" >&2
    exit 1
  fi
done

if grep -Fq 'spec:' "$post"; then
  echo "FAIL: language-only post should omit spec" >&2
  exit 1
fi

echo "PASS: new-post creates a language-only podcast summary"
