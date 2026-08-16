#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
site_dir=$(mktemp -d "${TMPDIR:-/tmp}/variant-notes-test.XXXXXX")
trap 'rm -rf "$site_dir"' EXIT

cd "$repo_dir"
bundle exec jekyll build --quiet --destination "$site_dir"

home_page="$site_dir/index.html"

if ! grep -Fq 'href="/lex-summary/collections/practice-notes/"' "$home_page"; then
  echo "FAIL: homepage does not link to the Practice Notes collection with the project base URL" >&2
  exit 1
fi

echo "PASS: homepage links to the Practice Notes collection"

collection_page="$site_dir/collections/practice-notes/index.html"

if [ ! -f "$collection_page" ]; then
  echo "FAIL: Practice Notes collection page was not generated" >&2
  exit 1
fi

for edition_path in \
  /lex-summary/articles/ship-small/en/short/ \
  /lex-summary/articles/ship-small/en/long/ \
  /lex-summary/articles/ship-small/zh/short/ \
  /lex-summary/articles/ship-small/zh/long/
do
  if ! grep -Fq "href=\"$edition_path\"" "$collection_page"; then
    echo "FAIL: collection page does not link to $edition_path" >&2
    exit 1
  fi
done

echo "PASS: collection page links to every article edition"

article_page="$site_dir/articles/ship-small/en/short/index.html"

if ! grep -Fq 'class="post-collection" href="/lex-summary/collections/practice-notes/"' "$article_page"; then
  echo "FAIL: article does not identify and link back to its collection" >&2
  exit 1
fi

echo "PASS: article links back to its collection"
