#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
site_dir=$(mktemp -d "${TMPDIR:-/tmp}/variant-notes-test.XXXXXX")
trap 'rm -rf "$site_dir"' EXIT

cd "$repo_dir"
bundle exec jekyll build --quiet --drafts --destination "$site_dir"

home_page="$site_dir/index.html"

if ! grep -Fq 'href="/lex-tldr/collections/practice-notes/"' "$home_page"; then
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
  /lex-tldr/articles/ship-small/en/ \
  /lex-tldr/articles/ship-small/cn/ \
  /lex-tldr/articles/spec-routing-example/en/long-guide/
do
  if ! grep -Fq "href=\"$edition_path\"" "$collection_page"; then
    echo "FAIL: collection page does not link to $edition_path" >&2
    exit 1
  fi
done

echo "PASS: collection page links to every article edition"

article_page="$site_dir/articles/ship-small/en/index.html"

if ! grep -Fq 'class="post-collection" href="/lex-tldr/collections/practice-notes/"' "$article_page"; then
  echo "FAIL: article does not identify and link back to its collection" >&2
  exit 1
fi

echo "PASS: article links back to its collection"

if grep -Fq '<span>Specification</span>' "$article_page"; then
  echo "FAIL: an edition without specs renders an empty specification field" >&2
  exit 1
fi

echo "PASS: article omits empty specification metadata"

long_article_page="$site_dir/articles/spec-routing-example/en/long-guide/index.html"

if ! grep -Fq 'EN · LONG / GUIDE' "$long_article_page"; then
  echo "FAIL: article does not render the ordered spec list" >&2
  exit 1
fi

echo "PASS: article renders the ordered spec list"
